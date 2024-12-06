import asyncio
from typing import Any, Dict, List, Optional, Union

import httpx


class PyletClient:
    def __init__(self, api_server_url: str = "http://localhost:8000"):
        self.api_server_url = api_server_url
        self.client = httpx.AsyncClient()

    async def submit_task(
        self,
        task_data: Union[str, List[str]],
        resource_requirements: Dict[str, int],
        name: Optional[str] = None,
    ) -> str:
        submission_data = {
            "task_data": task_data,
            "resource_requirements": resource_requirements,
        }
        if name:
            submission_data["name"] = name

        response = await self.client.post(
            f"{self.api_server_url}/tasks", json=submission_data
        )
        response.raise_for_status()
        task_id = response.json()["task_id"]
        return task_id

    async def get_task(self, task_id: str) -> Dict[str, Any]:
        response = await self.client.get(
            f"{self.api_server_url}/tasks/{task_id}"
        )
        response.raise_for_status()
        return response.json()

    async def get_task_by_name(self, name: str) -> Dict[str, Any]:
        response = await self.client.get(
            f"{self.api_server_url}/tasks/by-name/{name}"
        )
        response.raise_for_status()
        return response.json()

    async def get_task_result(self, task_id: str) -> Dict[str, Any]:
        response = await self.client.get(
            f"{self.api_server_url}/tasks/{task_id}/result"
        )
        if response.status_code == 202:
            return {"status": "PENDING"}
        response.raise_for_status()
        return response.json()

    async def list_workers(self) -> List[Dict[str, Any]]:
        response = await self.client.get(f"{self.api_server_url}/workers")
        response.raise_for_status()
        return response.json()

    async def get_worker(self, worker_id: str) -> Dict[str, Any]:
        response = await self.client.get(
            f"{self.api_server_url}/workers/{worker_id}"
        )
        response.raise_for_status()
        return response.json()

    async def close(self):
        await self.client.aclose()
