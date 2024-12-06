import asyncio
import random
import uuid
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Union

from pylet.logger import logger
from pylet.schemas import ResourceSpec, Task, TaskStatus, Worker


class Controller:
    def __init__(self):
        self.lock = asyncio.Lock()
        self.workers: Dict[str, Worker] = {}
        self.tasks: Dict[str, Task] = {}
        self.task_name_map = {}
        self.worker_task_queues: Dict[str, asyncio.Queue] = {}
        self.pending_tasks: asyncio.Queue = asyncio.Queue()
        self.HEARTBEAT_TIMEOUT = timedelta(seconds=15)

    # Task Management Methods

    async def submit_task(
        self,
        task_data: Union[str, List[str]],
        resource_requirements: ResourceSpec,
        name: Optional[str] = None,
    ) -> str:
        async with self.lock:
            task_id = str(uuid.uuid4())
            task = Task(
                task_id=task_id,
                name=name,
                task_data=task_data,
                resource_requirements=resource_requirements,
            )
            self.tasks[task_id] = task
            # If a name is provided, map the name to the task ID
            if name:
                if name in self.task_name_map:
                    # Handle duplicate names if needed
                    raise ValueError(
                        f"A task with name '{name}' already exists."
                    )
                self.task_name_map[name] = task_id
            logger.info(
                f"Task {task_id} ('{name}') submitted with requirements: {resource_requirements}"
            )
        return task_id

    async def get_task_result(self, task_id: str) -> Optional[Task]:
        async with self.lock:
            task = self.tasks.get(task_id)
            if task:
                logger.debug(f"Retrieved task {task_id} status: {task.status}.")
            else:
                logger.warning(f"Task {task_id} not found.")
            return task

    # Worker Management Methods

    async def register_worker(self, worker_id: str, resources: ResourceSpec):
        async with self.lock:
            if worker_id in self.workers:
                logger.warning(f"Worker {worker_id} already registered.")
                raise ValueError("Worker already registered")
            worker = Worker(
                worker_id=worker_id,
                total_resources=resources,
                available_resources=resources.copy(),
            )
            self.workers[worker_id] = worker
            self.worker_task_queues[worker_id] = asyncio.Queue()
            logger.info(
                f"Worker {worker_id} registered with resources: {resources}"
            )

    async def update_worker_heartbeat(self, worker_id: str):
        async with self.lock:
            worker = self.workers.get(worker_id)
            if not worker:
                logger.warning(
                    f"Heartbeat received from unregistered worker {worker_id}."
                )
                raise ValueError("Worker not registered")
            worker.last_seen = datetime.now()
            logger.debug(f"Heartbeat updated for worker {worker_id}.")

    async def get_task_for_worker(self, worker_id: str) -> Optional[Task]:
        async with self.lock:
            worker = self.workers.get(worker_id)
            if not worker:
                logger.warning(
                    f"Worker {worker_id} not registered when requesting task."
                )
                raise ValueError("Worker not registered")
            task_queue = self.worker_task_queues[worker_id]
        # Wait for a task assignment with an extended timeout
        try:
            task_id = await asyncio.wait_for(
                task_queue.get(), timeout=30
            )  # Extended timeout to 30 seconds
            async with self.lock:
                task = self.tasks.get(task_id)
                if task:
                    logger.info(f"Worker {worker_id} fetched task {task_id}.")
                else:
                    logger.error(
                        f"Task {task_id} not found for worker {worker_id}."
                    )
            return task
        except asyncio.TimeoutError:
            logger.debug(
                f"No task available for worker {worker_id} within timeout."
            )
            return None

    async def get_task_by_name(self, name: str) -> Optional[Task]:
        async with self.lock:
            task_id = self.task_name_map.get(name)
            if task_id:
                return self.tasks.get(task_id)
            else:
                return None

    async def report_task_result(
        self, worker_id: str, task_id: str, success: bool, result_data: str
    ):
        async with self.lock:
            task = self.tasks.get(task_id)
            if not task:
                logger.error(
                    f"Task {task_id} not found when worker {worker_id} reported result."
                )
                raise ValueError("Task not found")
            if task.assigned_to != worker_id:
                logger.warning(
                    f"Worker {worker_id} not assigned to task {task_id} but attempted to report result."
                )
                raise ValueError("Worker not assigned to this task")
            if success:
                task.status = TaskStatus.COMPLETED
                task.result_data = result_data
                logger.info(
                    f"Task {task_id} completed successfully by worker {worker_id}."
                )
            else:
                task.status = TaskStatus.FAILED
                task.result_data = result_data
                logger.info(f"Task {task_id} failed by worker {worker_id}.")
            # Release resources
            worker = self.workers.get(worker_id)
            if worker:
                worker.available_resources.cpu_cores += (
                    task.resource_requirements.cpu_cores
                )
                worker.available_resources.gpu_units += (
                    task.resource_requirements.gpu_units
                )
                worker.available_resources.memory_mb += (
                    task.resource_requirements.memory_mb
                )
                logger.debug(
                    f"Released resources for worker {worker_id}: {task.resource_requirements}"
                )

    async def get_task(self, task_id: str) -> Optional[Task]:
        async with self.lock:
            return self.tasks.get(task_id)

    async def get_all_workers(self) -> List[Worker]:
        async with self.lock:
            return list(self.workers.values())

    async def get_worker(self, worker_id: str) -> Optional[Worker]:
        async with self.lock:
            return self.workers.get(worker_id)

    # Internal Methods

    async def process_pending_tasks(self):
        while True:
            async with self.lock:
                pending_tasks = sorted(
                    (
                        task
                        for task in self.tasks.values()
                        if task.status == TaskStatus.PENDING
                    ),
                    key=lambda t: t.created_at,
                )
            for task in pending_tasks:
                async with self.lock:
                    assigned_worker = await self.schedule_task(task)
                    if assigned_worker:
                        await self.worker_task_queues[
                            assigned_worker.worker_id
                        ].put(task.task_id)
                        task.status = TaskStatus.ASSIGNED
                        task.assigned_to = assigned_worker.worker_id
                        # Update worker's available resources
                        assigned_worker.available_resources.cpu_cores -= (
                            task.resource_requirements.cpu_cores
                        )
                        assigned_worker.available_resources.gpu_units -= (
                            task.resource_requirements.gpu_units
                        )
                        assigned_worker.available_resources.memory_mb -= (
                            task.resource_requirements.memory_mb
                        )
                        logger.info(
                            f"Task {task.task_id} assigned to worker {assigned_worker.worker_id} in background scheduler."
                        )
                    else:
                        logger.debug(
                            f"No available workers to assign task {task.task_id}. Task remains pending."
                        )
            await asyncio.sleep(2)  # Adjust the sleep interval as needed

    async def schedule_task(self, task: Task) -> Optional[Worker]:
        """Assigns a task to a suitable worker based on resource requirements."""
        # Find workers with sufficient resources
        suitable_workers = []
        for worker in self.workers.values():
            if (
                worker.available_resources.cpu_cores
                >= task.resource_requirements.cpu_cores
                and worker.available_resources.gpu_units
                >= task.resource_requirements.gpu_units
                and worker.available_resources.memory_mb
                >= task.resource_requirements.memory_mb
                and datetime.now() - worker.last_seen < self.HEARTBEAT_TIMEOUT
            ):
                suitable_workers.append(worker)
        if not suitable_workers:
            logger.debug("No suitable workers available to schedule task.")
            return None
        # Randomly select a suitable worker
        assigned_worker = random.choice(suitable_workers)
        logger.debug(
            f"Scheduling task {task.task_id} to worker {assigned_worker.worker_id}."
        )
        return assigned_worker

    async def monitor_workers(self):
        while True:
            await asyncio.sleep(self.HEARTBEAT_INTERVAL)
            async with self.lock:
                for worker_id in list(self.workers):
                    worker = self.workers[worker_id]
                    if (
                        datetime.now() - worker.last_seen
                        > self.HEARTBEAT_TIMEOUT
                    ):
                        # Worker timed out
                        logger.warning(
                            f"Worker {worker_id} timed out: {worker.last_seen}"
                        )
                        del self.workers[worker_id]
                        del self.worker_task_queues[worker_id]
                        # Reassign tasks
                        await self.reassign_tasks(worker_id)

    async def update_task_status(
        self, worker_id: str, task_id: str, status_update: Dict[str, Any]
    ):
        async with self.lock:
            if task_id not in self.tasks:
                raise ValueError(f"Task {task_id} does not exist.")
            task = self.tasks[task_id]
            if task.assigned_to != worker_id:
                raise ValueError(
                    f"Task {task_id} is not assigned to worker {worker_id}."
                )
            # Update the task's status_info dictionary with the new status updates
            task.status_info.update(status_update)
            logger.debug(f"Task {task_id} status updated with {status_update}")

    async def reassign_tasks(self, timed_out_worker_id: str):
        for task in self.tasks.values():
            if (
                task.assigned_to == timed_out_worker_id
                and task.status == TaskStatus.ASSIGNED
            ):
                task.status = TaskStatus.PENDING
                task.assigned_to = None
                logger.info(
                    f"Task {task.task_id} reassigned from timed-out worker {timed_out_worker_id}."
                )
                # Release resources from timed-out worker
                worker = self.workers.get(timed_out_worker_id)
                if worker:
                    worker.available_resources.cpu_cores += (
                        task.resource_requirements.cpu_cores
                    )
                    worker.available_resources.gpu_units += (
                        task.resource_requirements.gpu_units
                    )
                    worker.available_resources.memory_mb += (
                        task.resource_requirements.memory_mb
                    )
                    logger.debug(
                        f"Released resources from timed-out worker {timed_out_worker_id}: {task.resource_requirements}"
                    )
                # Assign to another worker
                assigned_worker = await self.schedule_task(task)
                if assigned_worker:
                    await self.worker_task_queues[
                        assigned_worker.worker_id
                    ].put(task.task_id)
                    task.status = TaskStatus.ASSIGNED
                    task.assigned_to = assigned_worker.worker_id
                    # Update worker's available resources
                    assigned_worker.available_resources.cpu_cores -= (
                        task.resource_requirements.cpu_cores
                    )
                    assigned_worker.available_resources.gpu_units -= (
                        task.resource_requirements.gpu_units
                    )
                    assigned_worker.available_resources.memory_mb -= (
                        task.resource_requirements.memory_mb
                    )
                    logger.info(
                        f"Task {task.task_id} reassigned to worker {assigned_worker.worker_id}."
                    )
                else:
                    logger.warning(
                        f"No available workers to reassign task {task.task_id}. Task remains pending."
                    )
