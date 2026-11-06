
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    title: str = Field(
        min_length=1,
        max_length=200,
        description="Title of the task",
    )
    priority: Literal["low", "medium", "high"] = "medium"


class TaskResponse(BaseModel):
    id: int
    title: str
    priority: Literal["low", "medium", "high"]
    status: Literal["pending", "done"]
    created_at: datetime


class TaskListResponse(BaseModel):
    total: int
    tasks: list[TaskResponse]
