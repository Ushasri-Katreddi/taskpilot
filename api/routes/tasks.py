
from fastapi import APIRouter, HTTPException, Query
from fastmcp import Client

from api.schemas.tasks import TaskCreate, TaskListResponse, TaskResponse


router = APIRouter(
    prefix="/api/tasks",
    tags=["Tasks"],
)

TASKS_SERVER_URL = "http://127.0.0.1:8001/mcp"


async def call_tasks_tool(tool_name: str, arguments: dict):
    """
    Connect to the Tasks MCP server and execute a tool.

    A new client session is opened for each API request.
    """
    try:
        async with Client(TASKS_SERVER_URL) as client:
            result = await client.call_tool(tool_name, arguments)

            if result.is_error:
                error_message = str(result.content)
                raise HTTPException(
                    status_code=400,
                    detail=error_message,
                )

            return result.data

    except HTTPException:
        raise

    except Exception as error:
        raise HTTPException(
            status_code=502,
            detail=f"Tasks MCP server error: {str(error)}",
        ) from error


@router.get("", response_model=TaskListResponse)
async def get_tasks(
    status: str = Query(
        default="all",
        description="Filter tasks by all, pending, or done",
    )
):
    """Retrieve tasks, optionally filtered by status."""

    tasks = await call_tasks_tool(
        "list_tasks",
        {"status": status},
    )

    return {
        "total": len(tasks),
        "tasks": tasks,
    }


@router.get("/search", response_model=TaskListResponse)
async def search_tasks(
    keyword: str = Query(min_length=1)
):
    """Search tasks by title keyword."""

    tasks = await call_tasks_tool(
        "search_tasks",
        {"keyword": keyword},
    )

    return {
        "total": len(tasks),
        "tasks": tasks,
    }


@router.post("", response_model=TaskResponse, status_code=201)
async def create_task(task: TaskCreate):
    """Create a new task through the Tasks MCP server."""

    created_task = await call_tasks_tool(
        "add_task",
        {
            "title": task.title,
            "priority": task.priority,
        },
    )

    return created_task


@router.patch("/{task_id}/complete", response_model=TaskResponse)
async def complete_task(task_id: int):
    """Mark a task as completed."""

    completed_task = await call_tasks_tool(
        "complete_task",
        {"task_id": task_id},
    )

    return completed_task


@router.delete("/{task_id}")
async def delete_task(task_id: int):
    """Delete a task by its ID."""

    deleted_task = await call_tasks_tool(
        "delete_task",
        {"task_id": task_id},
    )

    return deleted_task
