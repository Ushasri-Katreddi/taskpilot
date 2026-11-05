
import sys
from pathlib import Path

import pytest
from fastmcp import Client
from fastmcp.client.transports import StdioTransport


# Resolve the TaskPilot project root
PROJECT_ROOT = Path(__file__).resolve().parents[1]


@pytest.mark.asyncio
async def test_math_mcp_client():
    """Connect to the Math MCP Server using STDIO transport."""

    transport = StdioTransport(
        command=sys.executable,
        args=["-m", "servers.math_server"],
        cwd=str(PROJECT_ROOT),
    )

    async with Client(transport) as client:

        # Discover available tools
        tools = await client.list_tools()

        tool_names = [tool.name for tool in tools]

        print("\nMath MCP Tools:", tool_names)

        assert "add" in tool_names
        assert "multiply" in tool_names
        assert "percentage" in tool_names

        # Execute every Math tool
        result = await client.call_tool(
            "add", {"a": 10, "b": 20}
        )
        assert result.data == 30

        result = await client.call_tool(
            "multiply", {"a": 5, "b": 4}
        )
        assert result.data == 20

        result = await client.call_tool(
            "percentage", {"value": 25, "total": 100}
        )
        assert result.data == 25

        print("Math MCP tools executed successfully.")


@pytest.mark.asyncio
async def test_tasks_mcp_client():
    """Connect to the Tasks MCP Server using HTTP transport."""

    async with Client("http://127.0.0.1:8001/mcp") as client:

        # 1. Discover tools
        tools = await client.list_tools()
        tool_names = [tool.name for tool in tools]

        print("\nTasks MCP Tools:", tool_names)

        assert "add_task" in tool_names
        assert "list_tasks" in tool_names
        assert "complete_task" in tool_names
        assert "delete_task" in tool_names
        assert "search_tasks" in tool_names

        # 2. Discover resources and resource templates
        resources = await client.list_resources()
        templates = await client.list_resource_templates()

        print(
            "\nResources:",
            [resource.uri for resource in resources],
        )
        print(
            "Resource Templates:",
            [template.uri_template for template in templates],
        )

        # 3. Discover prompts
        prompts = await client.list_prompts()

        print(
            "\nPrompts:",
            [prompt.name for prompt in prompts],
        )

        assert any(
            str(resource.uri) == "tasks://summary"
            for resource in resources
        )
        assert any(
            template.uri_template == "tasks://{task_id}"
            for template in templates
        )
        assert any(
            prompt.name == "daily plan"
            for prompt in prompts
        )

        # 4. Create a task
        result = await client.call_tool(
            "add_task",
            {
                "title": "Client integration verification",
                "priority": "high",
            },
        )

        task_id = result.data["id"]

        assert result.data["status"] == "pending"
        print("\nCreated Task:", result.data)

        # 5. List all tasks
        result = await client.call_tool(
            "list_tasks", {"status": "all"}
        )
        assert any(task["id"] == task_id for task in result.data)

        # 6. Search tasks
        result = await client.call_tool(
            "search_tasks",
            {"keyword": "integration verification"},
        )
        assert any(task["id"] == task_id for task in result.data)

        # 7. Read summary resource
        summary_result = await client.read_resource(
            "tasks://summary"
        )
        summary = __import__("json").loads(
            summary_result[0].text
        )

        print("\nTask Summary:", summary)
        assert summary["total"] >= 1

        # 8. Read individual task resource
        task_result = await client.read_resource(
            f"tasks://{task_id}"
        )
        task_details = __import__("json").loads(
            task_result[0].text
        )

        assert task_details["id"] == task_id
        print("\nTask Details:", task_details)

        # 9. Retrieve daily plan prompt
        prompt_result = await client.get_prompt(
            "daily plan",
            {"focus_area": "high priority tasks"},
        )

        assert len(prompt_result.messages) > 0
        print("\nDaily Plan Prompt retrieved.")

        # 10. Complete the task
        result = await client.call_tool(
            "complete_task", {"task_id": task_id}
        )
        assert result.data["status"] == "done"

        # 11. Verify completed tasks
        result = await client.call_tool(
            "list_tasks", {"status": "done"}
        )
        assert any(task["id"] == task_id for task in result.data)

        # 12. Delete the task
        result = await client.call_tool(
            "delete_task", {"task_id": task_id}
        )
        assert result.data["task"]["id"] == task_id

        print("\nAll Tasks MCP operations completed successfully.")
