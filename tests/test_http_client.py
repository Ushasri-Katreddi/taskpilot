
import json
import pytest
from fastmcp import Client


@pytest.mark.asyncio
async def test_tasks_http_connection():
    async with Client("http://127.0.0.1:8001/mcp") as client:

        # 1. Discover tools
        tools = await client.list_tools()

        print("\nAvailable Tools:")
        for tool in tools:
            print(tool.name)

        assert len(tools) == 5

        # 2. Create a task
        result = await client.call_tool(
            "add_task",
            {
                "title": "Test HTTP MCP integration",
                "priority": "high",
            },
        )

        task_id = result.data["id"]
        print("\nCreated Task:", result.data)

        # 3. List pending tasks
        result = await client.call_tool(
            "list_tasks",
            {"status": "pending"},
        )

        assert any(task["id"] == task_id for task in result.data)

        # 4. Read the task summary resource
        summary_result = await client.read_resource(
            "tasks://summary"
        )

        summary = json.loads(summary_result[0].text)

        print("\nTask Summary:", summary)

        assert summary["total"] >= 1
        assert summary["pending"] >= 1

        # 5. Read the individual task resource
        task_result = await client.read_resource(
            f"tasks://{task_id}"
        )

        task_details = json.loads(task_result[0].text)

        print("\nIndividual Task:", task_details)

        assert task_details["id"] == task_id

        # 6. Retrieve the daily plan prompt
        prompt_result = await client.get_prompt(
            "daily plan",
            {"focus_area": "high priority tasks"},
        )

        print("\nDaily Plan Prompt:")
        print(prompt_result.messages)

        assert len(prompt_result.messages) > 0

        print("\nAll HTTP MCP tests completed successfully!")
