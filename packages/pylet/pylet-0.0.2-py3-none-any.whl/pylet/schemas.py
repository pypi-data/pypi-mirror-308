from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field


class ResourceSpec(BaseModel):
    cpu_cores: int
    gpu_units: int
    memory_mb: int


class TaskStatus(str, Enum):
    PENDING = "PENDING"
    ASSIGNED = "ASSIGNED"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class Task(BaseModel):
    task_id: str
    name: Optional[str] = None  # New field for task name
    task_data: Union[str, List[str]]
    resource_requirements: ResourceSpec
    status: TaskStatus = TaskStatus.PENDING
    assigned_to: Optional[str] = None
    result_data: Optional[Any] = None
    status_info: Dict[str, Any] = {}
    created_at: datetime = Field(default_factory=datetime.now)


class Worker(BaseModel):
    worker_id: str
    total_resources: ResourceSpec
    available_resources: ResourceSpec
    last_seen: datetime = Field(default_factory=datetime.now)


class TaskSubmissionRequest(BaseModel):
    task_data: Union[
        str, List[str]
    ]  # Accept either a string or a list of strings
    resource_requirements: ResourceSpec
    name: Optional[str] = None  # Added to match submission
