
import json
from datetime import datetime, timezone
from pathlib import Path

from fastmcp import FastMCP, Context


# --------------------------------------------------
# 1. Initialize MCP server
# --------------------------------------------------

mcp = FastMCP(
    name="Tasks MCP Server",
    instructions=(
        "A task management server that supports creating, "
        "listing, updating, deleting, and searching tasks."
    ),
)


# --------------------------------------------------
# 2. JSON storage configuration
# --------------------------------------------------

DATA_FILE = Path(__file__).resolve().parents[1] / "data" / "tasks.json"


def load_tasks() -> list[dict]:
    """Load tasks from the JSON file."""

    if not DATA_FILE.exists():
        DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
        DATA_FILE.write_text(
            json.dumps({"tasks": []}, indent=4),
            encoding="utf-8",
        )

    with DATA_FILE.open("r", encoding="utf-8") as file:
        data = json.load(file)

    return data.get("tasks", [])


def save_tasks(tasks: list[dict]) -> None:
    """Persist tasks to the JSON file."""

    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)

    with DATA_FILE.open("w", encoding="utf-8") as file:
        json.dump({"tasks": tasks}, file, indent=4)


def get_next_task_id(tasks: list[dict]) -> int:
    """Generate the next available task ID."""

    if not tasks:
        return 1

    return max(task["id"] for task in tasks) + 1


# --------------------------------------------------
# 3. Add task tool
# --------------------------------------------------

@mcp.tool()
async def add_task(
    title: str,
    priority: str,
    ctx: Context,
) -> dict:
    """
    Create a new task with a title and priority.

    Args:
        title: Description of the task.
        priority: Task priority - low, medium, or high.
    """

    if not title.strip():
        raise ValueError("Task title cannot be empty.")

    if priority not in {"low", "medium", "high"}:
        raise ValueError(
            "Invalid priority. Choose low, medium, or high."
        )

    tasks = load_tasks()

    new_task = {
        "id": get_next_task_id(tasks),
        "title": title.strip(),
        "priority": priority,
        "status": "pending",
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    tasks.append(new_task)
    save_tasks(tasks)

    await ctx.info(f"Created task with ID {new_task['id']}")

    return new_task


# --------------------------------------------------
# 4. List tasks tool
# --------------------------------------------------

@mcp.tool()
def list_tasks(status: str = "all") -> list[dict]:
    """
    List tasks filtered by status.

    Args:
        status: Filter - all, pending, or done.
    """

    if status not in {"all", "pending", "done"}:
        raise ValueError(
            "Invalid status. Choose all, pending, or done."
        )

    tasks = load_tasks()

    if status == "all":
        return tasks

    return [
        task for task in tasks
        if task["status"] == status
    ]


# --------------------------------------------------
# 5. Mark task as completed
# --------------------------------------------------

@mcp.tool()
def complete_task(task_id: int) -> dict:
    """
    Mark a task as completed using its ID.

    Args:
        task_id: ID of the task to complete.
    """

    tasks = load_tasks()

    for task in tasks:
        if task["id"] == task_id:
            task["status"] = "done"
            save_tasks(tasks)

            return task

    raise ValueError(f"Task with ID {task_id} not found.")


# --------------------------------------------------
# 6. Delete task tool
# --------------------------------------------------

@mcp.tool()
def delete_task(task_id: int) -> dict:
    """
    Delete a task using its ID.

    Args:
        task_id: ID of the task to delete.
    """

    tasks = load_tasks()

    for index, task in enumerate(tasks):
        if task["id"] == task_id:
            deleted_task = tasks.pop(index)
            save_tasks(tasks)

            return {
                "message": "Task deleted successfully.",
                "task": deleted_task,
            }

    raise ValueError(f"Task with ID {task_id} not found.")


# --------------------------------------------------
# 7. Search tasks tool
# --------------------------------------------------

@mcp.tool()
def search_tasks(keyword: str) -> list[dict]:
    """
    Search tasks by a keyword in their titles.

    Args:
        keyword: Text to search for in task titles.
    """

    if not keyword.strip():
        raise ValueError("Search keyword cannot be empty.")

    tasks = load_tasks()
    search_term = keyword.strip().lower()

    return [
        task for task in tasks
        if search_term in task["title"].lower()
    ]


# --------------------------------------------------
# 8. Static summary resource
# --------------------------------------------------

@mcp.resource("tasks://summary")
def get_task_summary() -> str:
    """Return total, completed, and pending task counts."""

    tasks = load_tasks()

    completed = sum(
        1 for task in tasks
        if task["status"] == "done"
    )

    pending = sum(
        1 for task in tasks
        if task["status"] == "pending"
    )

    summary = {
        "total": len(tasks),
        "completed": completed,
        "pending": pending,
    }

    return json.dumps(summary, indent=4)


# --------------------------------------------------
# 9. Dynamic task resource template
# --------------------------------------------------

@mcp.resource("tasks://{task_id}")
def get_task_by_id(task_id: int) -> str:
    """Retrieve an individual task using its ID."""

    tasks = load_tasks()

    for task in tasks:
        if task["id"] == task_id:
            return json.dumps(task, indent=4)

    raise ValueError(f"Task with ID {task_id} not found.")


# --------------------------------------------------
# 10. Daily plan prompt
# --------------------------------------------------

@mcp.prompt(name="daily plan")
def daily_plan(focus_area: str) -> str:
    """
    Generate a daily plan based on pending tasks.

    Args:
        focus_area: Area the user wants to focus on today.
    """

    tasks = [
        task for task in load_tasks()
        if task["status"] == "pending"
    ]

    pending_tasks = json.dumps(tasks, indent=4)

    return (
        f"Create a practical daily plan focused on: {focus_area}.\n\n"
        f"Here are the user's pending tasks:\n{pending_tasks}\n\n"
        "Prioritize high-priority tasks first. "
        "Organize the tasks into a realistic schedule. "
        "Do not include completed tasks."
    )


# --------------------------------------------------
# 11. Start HTTP MCP server
# --------------------------------------------------

if __name__ == "__main__":
    mcp.run(transport="http", host="127.0.0.1", port=8001)
