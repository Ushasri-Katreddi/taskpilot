
import asyncio

from langchain.mcp import MCPAdapter
from langgraph.checkpoint.memory import InMemorySaver

from client.agent import create_taskpilot_agent
from client.mcp_config import MCP_SERVERS_CONFIG


async def main():

    # Initialize conversation memory
    checkpointer = InMemorySaver()

    async with MCPAdapter(MCP_SERVERS_CONFIG) as adapter:

        # Dynamically discover MCP tools
        tools = await adapter.list_tools()

        # Create agent with memory
        agent = create_taskpilot_agent(
            tools,
            checkpointer=checkpointer,
        )

        # Unique conversation identifier
        config = {
            "configurable": {
                "thread_id": "taskpilot-memory-test-1"
            }
        }

        # First conversation turn
        print("\nUSER: Create a high-priority task called Prepare report.")

        response1 = await agent.ainvoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": "Create a high-priority task called Prepare report."
                    }
                ]
            },
            config=config,
        )

        print("\nTASKPILOT:")
        print(response1["messages"][-1].content)

        # Second conversation turn
        print("\nUSER: Mark that task as completed.")

        response2 = await agent.ainvoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": "Mark that task as completed."
                    }
                ]
            },
            config=config,
        )

        print("\nTASKPILOT:")
        print(response2["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())
