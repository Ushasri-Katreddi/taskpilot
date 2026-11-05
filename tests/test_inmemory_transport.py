
import pytest
from fastmcp import Client
from servers.tasks_server import mcp


@pytest.mark.asyncio
async def test_tasks_inmemory_transport():
    """Test Tasks MCP Server using in-memory transport."""

    async with Client(mcp) as client:

        # Discover tools
        tools = await client.list_tools()
        tool_names = [tool.name for tool in tools]

        print("\nAvailable tools:", tool_names)

        assert "add_task" in tool_names
        assert "list_tasks" in tool_names

        # Create a task
        result = await client.call_tool(
            "add_task",
            {
                "title": "In-memory transport test",
                "priority": "medium",
            },
        )

        task_id = result.data["id"]

        print("\nCreated task:", result.data)

        # Retrieve the task
        result = await client.call_tool(
            "list_tasks",
            {"status": "pending"},
        )

        assert any(
            task["id"] == task_id
            for task in result.data
        )

        # Delete the test task
        result = await client.call_tool(
            "delete_task",
            {"task_id": task_id},
        )

        assert result.data["task"]["id"] == task_id

        print("\nIn-memory transport test successful!")
