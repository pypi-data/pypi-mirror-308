# server.py

import asyncio
from contextlib import asynccontextmanager
from typing import Any, Dict, List, Optional, Union

from fastapi import FastAPI, HTTPException
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from fastapi.responses import JSONResponse, Response
from pydantic import BaseModel

from pylet.controller import Controller
from pylet.logger import logger  # Import the 'pylet' logger
from pylet.schemas import ResourceSpec, TaskStatus


class WorkerRegistrationRequest(BaseModel):
    worker_id: str
    resources: ResourceSpec


class TaskSubmissionRequest(BaseModel):
    name: Optional[str] = None  # New field for task name
    task_data: Union[str, List[str]]
    resource_requirements: ResourceSpec


class TaskResultReport(BaseModel):
    success: bool
    result_data: Optional[Any] = None


controller = Controller()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup code
    logger.info("Starting pylet server.")
    monitor_task = asyncio.create_task(controller.monitor_workers())
    scheduler_task = asyncio.create_task(controller.process_pending_tasks())
    try:
        yield
    finally:
        # Shutdown code
        logger.info("Shutting down pylet server.")
        monitor_task.cancel()
        scheduler_task.cancel()
        try:
            await monitor_task
            await scheduler_task
        except asyncio.CancelledError:
            pass


app = FastAPI(lifespan=lifespan)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request, exc: RequestValidationError
):
    logger.error(f"Validation error for request {request.url}: {exc}")
    return JSONResponse(
        status_code=422,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )


# Client Endpoints


@app.post("/tasks")
async def submit_task(submission_request: TaskSubmissionRequest):
    try:
        task_id = await controller.submit_task(
            submission_request.task_data,
            submission_request.resource_requirements,
            name=submission_request.name,
        )
        logger.info(
            f"Client submitted task {task_id} ('{submission_request.name}') with requirements: {submission_request.resource_requirements}"
        )
        return {"task_id": task_id}
    except ValueError as e:
        logger.error(f"Error submitting task: {e}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Error submitting task: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/tasks/{task_id}")
async def get_task_details(task_id: str):
    task = await controller.get_task(task_id)
    if not task:
        logger.warning(f"Client requested non-existent task {task_id}.")
        raise HTTPException(status_code=404, detail="Task not found")
    # Return the task details, including status_info
    return {
        "task_id": task.task_id,
        "status": task.status,
        "assigned_to": task.assigned_to,
        "status_info": task.status_info,
        "result_data": task.result_data,
    }


@app.get("/tasks/by-name/{task_name}")
async def get_task_by_name(task_name: str):
    task = await controller.get_task_by_name(task_name)
    if not task:
        logger.warning(
            f"Client requested non-existent task with name '{task_name}'."
        )
        raise HTTPException(status_code=404, detail="Task not found")
    # Return task details
    return {
        "task_id": task.task_id,
        "name": task.name,
        "status": task.status,
        "assigned_to": task.assigned_to,
        "status_info": task.status_info,
        "result_data": task.result_data,
    }


@app.get("/tasks/{task_id}/result")
async def get_task_result(task_id: str):
    task = await controller.get_task_result(task_id)
    if not task:
        logger.warning(f"Client requested non-existent task {task_id}.")
        raise HTTPException(status_code=404, detail="Task not found")
    if task.status == TaskStatus.COMPLETED:
        logger.info(f"Client retrieved result for task {task_id}.")
        return {"result": task.result_data}
    elif task.status == TaskStatus.FAILED:
        logger.info(f"Client retrieved failure for task {task_id}.")
        return {"error": task.result_data}
    else:
        logger.debug(f"Client requested incomplete task {task_id}.")
        raise HTTPException(status_code=202, detail="Task not yet completed")


# Worker Endpoints


@app.post("/workers")
async def register_worker(registration_request: WorkerRegistrationRequest):
    try:
        await controller.register_worker(
            registration_request.worker_id, registration_request.resources
        )
        logger.info(
            f"Worker {registration_request.worker_id} registered via API."
        )
        return {"message": "Worker registered successfully"}
    except ValueError as e:
        logger.warning(
            f"Worker registration failed for {registration_request.worker_id}: {e}"
        )
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/workers")
async def get_workers():
    workers = await controller.get_all_workers()
    # Convert workers to serializable format if necessary
    return [worker.dict() for worker in workers]


@app.get("/workers/{worker_id}")
async def get_worker(worker_id: str):
    worker = await controller.get_worker(worker_id)
    if not worker:
        logger.warning(f"Requested non-existent worker {worker_id}.")
        raise HTTPException(status_code=404, detail="Worker not found")
    return worker.dict()


@app.post("/workers/{worker_id}/heartbeat")
async def worker_heartbeat(worker_id: str):
    try:
        await controller.update_worker_heartbeat(worker_id)
        logger.debug(f"Heartbeat received from worker {worker_id}.")
        return {"message": "Heartbeat received"}
    except ValueError as e:
        logger.warning(f"Heartbeat error for worker {worker_id}: {e}")
        raise HTTPException(status_code=404, detail=str(e))


@app.get("/workers/{worker_id}/tasks")
async def get_task_for_worker_endpoint(worker_id: str):
    try:
        task = await controller.get_task_for_worker(worker_id)
        if task:
            logger.info(
                f"Worker {worker_id} fetched task {task.task_id} via API."
            )
            return {"task_id": task.task_id, "task_data": task.task_data}
        else:
            logger.debug(f"No task assigned to worker {worker_id}.")
            # Return HTTP 204 No Content to indicate no task is available
            return Response(status_code=204)
    except ValueError as e:
        logger.warning(f"Task fetch error for worker {worker_id}: {e}")
        raise HTTPException(status_code=404, detail=str(e))


@app.post("/workers/{worker_id}/tasks/{task_id}/status")
async def report_task_status_endpoint(
    worker_id: str, task_id: str, status_update: Dict[str, Any]
):
    try:
        await controller.update_task_status(worker_id, task_id, status_update)
        logger.info(
            f"Worker {worker_id} reported status for task {task_id}: {status_update}"
        )
        return {"message": "Status update received"}
    except ValueError as e:
        logger.warning(
            f"Status report error for worker {worker_id}, task {task_id}: {e}"
        )
        raise HTTPException(status_code=400, detail=str(e))


@app.post("/workers/{worker_id}/tasks/{task_id}/result")
async def report_task_result_endpoint(
    worker_id: str, task_id: str, report: TaskResultReport
):
    try:
        await controller.report_task_result(
            worker_id, task_id, report.success, report.result_data
        )
        logger.info(
            f"Worker {worker_id} reported result for task {task_id} via API."
        )
        return {"message": "Result received"}
    except ValueError as e:
        logger.warning(
            f"Result report error for worker {worker_id}, task {task_id}: {e}"
        )
        raise HTTPException(status_code=400, detail=str(e))
