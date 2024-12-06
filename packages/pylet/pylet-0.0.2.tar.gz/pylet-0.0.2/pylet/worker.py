# worker.py

import asyncio
import json
import os
import uuid

import httpx

from pylet.logger import logger


class Worker:
    def __init__(self, head_address, cpu_cores=4, gpu_units=0, memory_mb=4096):
        self.worker_id = str(uuid.uuid4())
        self.head_address = head_address
        self.api_server_url = f"http://{head_address}"
        self.total_resources = {
            "cpu_cores": cpu_cores,
            "gpu_units": gpu_units,
            "memory_mb": memory_mb,
        }
        self.available_ports = asyncio.Queue()
        self.port_range = (15600, 15700)
        self.max_concurrent_tasks = min(
            cpu_cores, self.port_range[1] - self.port_range[0] + 1
        )

    async def initialize_port_pool(self):
        for port in range(self.port_range[0], self.port_range[1] + 1):
            await self.available_ports.put(port)

    async def run(self):
        await self.initialize_port_pool()
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.api_server_url}/workers",
                    json={
                        "worker_id": self.worker_id,
                        "resources": self.total_resources,
                    },
                )
                response.raise_for_status()
                logger.info(
                    f"Worker {self.worker_id} registered successfully with resources: {self.total_resources}"
                )
            except Exception as e:
                logger.error(f"Failed to register worker {self.worker_id}: {e}")
                return

            asyncio.create_task(self.send_heartbeat(client))
            task_queue = asyncio.Queue()
            asyncio.create_task(self.fetch_tasks(client, task_queue))
            semaphore = asyncio.Semaphore(self.max_concurrent_tasks)
            await self.execute_tasks(task_queue, semaphore, client)

    async def fetch_tasks(self, client, task_queue):
        while True:
            try:
                response = await client.get(
                    f"{self.api_server_url}/workers/{self.worker_id}/tasks",
                    timeout=35,
                )
                if response.status_code == 200:
                    data = response.json()
                    task_id = data["task_id"]
                    task_data = data["task_data"]
                    logger.info(
                        f"Worker {self.worker_id} received task {task_id}: {task_data}"
                    )
                    await task_queue.put((task_id, task_data))
                elif response.status_code == 204:
                    logger.debug(
                        f"No task assigned to worker {self.worker_id}. Retrying..."
                    )
                    await asyncio.sleep(1)
                else:
                    logger.error(
                        f"Unexpected response: {response.status_code} - {response.text}"
                    )
                    await asyncio.sleep(5)
            except httpx.TimeoutException:
                logger.debug(
                    f"Request timeout when fetching tasks for worker {self.worker_id}. Retrying..."
                )
                await asyncio.sleep(1)
            except Exception as e:
                logger.error(f"Error fetching task: {e}")
                await asyncio.sleep(5)

    async def execute_tasks(self, task_queue, semaphore, client):
        while True:
            task_id, task_data = await task_queue.get()
            await semaphore.acquire()
            port = await self.available_ports.get()
            asyncio.create_task(
                self.execute_and_report_task(
                    client, task_id, task_data, semaphore, port
                )
            )

    async def execute_and_report_task(
        self, client, task_id, task_data, semaphore, port
    ):
        try:
            logger.info(
                f"Worker {self.worker_id} executing task {task_id} on port {port}: {task_data}"
            )
            await self.report_task_status(
                client, task_id, {"port": port, "status": "RUNNING"}
            )
            result_data = await self.execute_task(task_data, task_id, port)
            await self.report_task_result(client, task_id, True, result_data)
        except Exception as e:
            logger.error(f"Error executing task {task_id}: {e}")
            error_data = {"error": str(e)}
            await self.report_task_result(client, task_id, False, error_data)
        finally:
            semaphore.release()
            await self.available_ports.put(port)

    async def execute_task(self, task_data, task_id, port):
        log_filename = f"task_{task_id}.log"
        err_filename = f"task_{task_id}.err"

        if isinstance(task_data, str):
            command = task_data.strip().split()
        elif isinstance(task_data, list):
            command = task_data
        else:
            raise ValueError(
                "Invalid task_data format. Expected a string or a list."
            )

        try:
            log_file = open(log_filename, "w")
            err_file = open(err_filename, "w")
            env = os.environ.copy()
            env["PORT"] = str(port)

            process = await asyncio.create_subprocess_exec(
                *command,
                stdout=log_file,
                stderr=err_file,
                env=env,
            )
            returncode = await process.wait()
            log_file.close()
            err_file.close()

            result = {
                "returncode": returncode,
                "stdout_log": log_filename,
                "stderr_log": err_filename,
                "port": port,
            }
            return result
        except Exception as e:
            try:
                log_file.close()
                err_file.close()
            except:
                pass
            logger.error(f"Error executing task {task_id}: {e}")
            raise e

    async def report_task_status(self, client, task_id, status_update):
        try:
            response = await client.post(
                f"{self.api_server_url}/workers/{self.worker_id}/tasks/{task_id}/status",
                json=status_update,
            )
            response.raise_for_status()
            logger.info(
                f"Worker {self.worker_id} reported status for task {task_id}: {status_update}"
            )
        except Exception as e:
            logger.error(f"Error reporting status for task {task_id}: {e}")

    async def report_task_result(self, client, task_id, success, result_data):
        try:
            response = await client.post(
                f"{self.api_server_url}/workers/{self.worker_id}/tasks/{task_id}/result",
                json={"success": success, "result_data": result_data},
            )
            response.raise_for_status()
            logger.info(
                f"Worker {self.worker_id} reported result for task {task_id}."
            )
        except Exception as e:
            logger.error(f"Error reporting result for task {task_id}: {e}")

    async def send_heartbeat(self, client):
        while True:
            await asyncio.sleep(5)
            try:
                response = await client.post(
                    f"{self.api_server_url}/workers/{self.worker_id}/heartbeat"
                )
                response.raise_for_status()
                logger.debug(f"Heartbeat sent from worker {self.worker_id}.")
            except Exception as e:
                logger.error(
                    f"Heartbeat error for worker {self.worker_id}: {e}"
                )
                break


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Worker class-based refactor")
    parser.add_argument(
        "head_address", type=str, help="Address of the head node"
    )
    parser.add_argument(
        "--cpu-cores", type=int, default=4, help="Number of CPU cores"
    )
    parser.add_argument(
        "--gpu-units", type=int, default=0, help="Number of GPU units"
    )
    parser.add_argument(
        "--memory-mb", type=int, default=4096, help="Amount of memory in MB"
    )
    args = parser.parse_args()

    worker = Worker(
        args.head_address, args.cpu_cores, args.gpu_units, args.memory_mb
    )
    asyncio.run(worker.run())
