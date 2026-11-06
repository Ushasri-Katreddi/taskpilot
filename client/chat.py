
import asyncio

from fastmcp import Client
from langchain.mcp import MCPAdapter
from langgraph.checkpoint.memory import InMemorySaver

from client.agent import create_taskpilot_agent
from client.mcp_config import MCP_SERVERS_CONFIG, TASKS_SERVER_URL


def display_tool_calls(messages):
    """Display only the tool calls from the current interaction."""

    for message in messages:
        tool_calls = getattr(message, "tool_calls", [])

        for tool_call in tool_calls:
            print(f"\n[TOOL CALLED] {tool_call['name']}")
            print(f"Arguments: {tool_call['args']}")


async def handle_summary(tasks_client):
    """Retrieve task statistics directly from the summary resource."""

    result = await tasks_client.read_resource("tasks://summary")

    print("\nTASK SUMMARY:")

    for content in result:
        if hasattr(content, "text"):
            print(content.text)


async def handle_task(tasks_client, task_id):
    """Retrieve an individual task using its resource template."""

    result = await tasks_client.read_resource(
        f"tasks://{task_id}"
    )

    print(f"\nTASK DETAILS - ID {task_id}:")

    for content in result:
        if hasattr(content, "text"):
            print(content.text)


async def handle_plan(tasks_client, agent, focus, config):
    """Retrieve the daily plan prompt and pass it to the agent."""

    prompt_result = await tasks_client.get_prompt(
        "daily plan",
        {"focus_area": focus},
    )

    prompt_text = "\n".join(
        message.content.text
        for message in prompt_result.messages
        if hasattr(message.content, "text")
    )

    response = await agent.ainvoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": prompt_text,
                }
            ]
        },
        config=config,
    )

    print("\nTASKPILOT DAILY PLAN:")

    print(response["messages"][-1].content)


async def main():

    # Initialize in-memory conversation persistence
    checkpointer = InMemorySaver()

    # Connect to both MCP systems
    async with MCPAdapter(MCP_SERVERS_CONFIG) as adapter:
        async with Client(TASKS_SERVER_URL) as tasks_client:

            print("Discovering MCP tools...")

            tools = await adapter.list_tools()

            print(f"Loaded {len(tools)} tools successfully.")

            # Create the TaskPilot agent
            agent = create_taskpilot_agent(
                tools,
                checkpointer=checkpointer,
            )

            # Maintain one conversation thread
            config = {
                "configurable": {
                    "thread_id": "taskpilot-terminal-session"
                }
            }

            # Track messages already displayed
            response_history = []

            print("\n================================")
            print("       TASKPILOT AI ASSISTANT")
            print("================================")
            print("\nAvailable commands:")
            print("  /summary       - View task statistics")
            print("  /task <id>     - View individual task details")
            print("  /plan <focus>  - Generate a daily plan")
            print("  exit           - End the session")

            while True:

                user_input = input("\nYOU: ").strip()

                if user_input.lower() in {"exit", "quit"}:
                    print("\nTaskPilot session ended.")
                    break

                if not user_input:
                    continue

                try:

                    # Direct resource retrieval: no LLM call
                    if user_input == "/summary":
                        await handle_summary(tasks_client)
                        continue

                    # Individual task resource retrieval
                    if user_input.startswith("/task"):

                        parts = user_input.split(maxsplit=1)

                        if len(parts) != 2 or not parts[1].isdigit():
                            print("Usage: /task <id>")
                            continue

                        await handle_task(
                            tasks_client,
                            int(parts[1]),
                        )
                        continue

                    # Retrieve reusable prompt and invoke agent
                    if user_input.startswith("/plan"):

                        parts = user_input.split(maxsplit=1)

                        if len(parts) != 2:
                            print("Usage: /plan <focus>")
                            continue

                        response = await agent.ainvoke(
                            {
                                "messages": [
                                    {
                                        "role": "user",
                                        "content": (
                                            await tasks_client.get_prompt(
                                                "daily plan",
                                                {"focus_area": parts[1]},
                                            )
                                        ).messages[0].content.text,
                                    }
                                ]
                            },
                            config=config,
                        )

                        print("\nTASKPILOT DAILY PLAN:")
                        print(response["messages"][-1].content)

                        response_history = response["messages"]
                        continue

                    # Record the previous message count
                    previous_message_count = len(response_history)

                    # Send normal requests to the agent
                    response = await agent.ainvoke(
                        {
                            "messages": [
                                {
                                    "role": "user",
                                    "content": user_input,
                                }
                            ]
                        },
                        config=config,
                    )

                    # Display only messages from this interaction
                    new_messages = response["messages"][
                        previous_message_count:
                    ]

                    display_tool_calls(new_messages)

                    print("\nTASKPILOT:")
                    print(response["messages"][-1].content)

                    # Update message history
                    response_history = response["messages"]

                except Exception as error:
                    print(f"\nSomething went wrong: {error}")

    print("\nAll MCP connections closed.")


if __name__ == "__main__":
    asyncio.run(main())
