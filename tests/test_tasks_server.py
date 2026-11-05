
import json

import pytest
from fastmcp import Client

from servers.tasks_server import mcp


@pytest.mark.asyncio
async def test_tasks_tools_and_resources():
    async with Client(mcp) as client:

        # 1. Add a task
        result = await client.call_tool(
            "add_task",
            {"title": "Complete project documentation", "priority": "high"},
        )
        assert result.data["id"] >= 1
        assert result.data["title"] == "Complete project documentation"

        task_id = result.data["id"]

        # 2. List all tasks
        result = await client.call_tool("list_tasks", {"status": "all"})
        assert any(task["id"] == task_id for task in result.data)

        # 3. List pending tasks
        result = await client.call_tool(
            "list_tasks", {"status": "pending"}
        )
        assert any(task["id"] == task_id for task in result.data)

        # 4. Search tasks
        result = await client.call_tool(
            "search_tasks", {"keyword": "documentation"}
        )
        assert any(task["id"] == task_id for task in result.data)

        # 5. Complete task
        result = await client.call_tool(
            "complete_task", {"task_id": task_id}
        )
        assert result.data["status"] == "done"

        # 6. Verify completed filter
        result = await client.call_tool(
            "list_tasks", {"status": "done"}
        )
        assert any(task["id"] == task_id for task in result.data)

        # 7. Read summary resource
        result = await client.read_resource("tasks://summary")
        summary = json.loads(result[0].text)

        assert summary["total"] >= 1
        assert summary["completed"] >= 1

        # 8. Read individual task resource
        result = await client.read_resource(f"tasks://{task_id}")
        task_details = json.loads(result[0].text)

        assert task_details["id"] == task_id

        # 9. Get daily plan prompt
        result = await client.get_prompt(
            "daily plan",
            {"focus_area": "project development"},
        )
        assert len(result.messages) > 0

        # 10. Delete task
        result = await client.call_tool(
            "delete_task", {"task_id": task_id}
        )
        assert result.data["task"]["id"] == task_id


@pytest.mark.asyncio
async def test_invalid_priority():
    async with Client(mcp) as client:
        result = await client.call_tool(
            "add_task",
            {"title": "Invalid priority test", "priority": "urgent"},
            raise_on_error=False,
        )

        assert result.is_error


@pytest.mark.asyncio
async def test_missing_task():
    async with Client(mcp) as client:
        result = await client.call_tool(
            "complete_task",
            {"task_id": 99999},
            raise_on_error=False,
        )

        assert result.is_error
