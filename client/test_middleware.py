
import asyncio

from langchain.mcp import MCPAdapter
from langgraph.checkpoint.memory import InMemorySaver

from client.agent import create_taskpilot_agent
from client.mcp_config import MCP_SERVERS_CONFIG


async def main():
    checkpointer = InMemorySaver()

    async with MCPAdapter(MCP_SERVERS_CONFIG) as adapter:
        tools = await adapter.list_tools()

        agent = create_taskpilot_agent(
            tools,
            checkpointer=checkpointer,
        )

        config = {
            "configurable": {
                "thread_id": "middleware-test-1"
            }
        }

        queries = [
            "Complete task 99.",
            "Create a task called Test validation with urgent priority."
        ]

        for query in queries:
            print(f"\nUSER: {query}")

            response = await agent.ainvoke(
                {
                    "messages": [
                        {"role": "user", "content": query}
                    ]
                },
                config=config,
            )

            print("\nTASKPILOT:")
            print(response["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())
