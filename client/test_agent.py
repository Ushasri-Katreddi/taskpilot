
import asyncio

from langchain.mcp import MCPAdapter

from client.agent import create_taskpilot_agent
from client.mcp_config import MCP_SERVERS_CONFIG


async def run_query(agent, query: str):
    """Run a query and display the agent's tool calls and response."""

    print(f"\n{'=' * 60}")
    print(f"USER: {query}")
    print("=" * 60)

    response = await agent.ainvoke(
        {
            "messages": [
                {"role": "user", "content": query}
            ]
        }
    )

    # Display tools selected by the LLM
    for message in response["messages"]:
        if getattr(message, "tool_calls", None):
            for tool_call in message.tool_calls:
                print(
                    f"\nTOOL CALLED: {tool_call['name']}"
                )
                print("Arguments:", tool_call["args"])

    # Display final response
    print("\nTASKPILOT:")
    print(response["messages"][-1].content)


async def main():

    async with MCPAdapter(MCP_SERVERS_CONFIG) as adapter:

        tools = await adapter.list_tools()

        print("\nDiscovered MCP Tools:")
        for tool in tools:
            print("-", tool.name)

        agent = create_taskpilot_agent(tools)

        # Test 1: Percentage calculation
        await run_query(
            agent,
            "Calculate 25 percent of 200."
        )

        # Test 2: Multiplication
        await run_query(
            agent,
            "Multiply 25 by 4."
        )

        # Test 3: Task management
        await run_query(
            agent,
            "List all my pending tasks."
        )


if __name__ == "__main__":
    asyncio.run(main())
