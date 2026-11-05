
import asyncio

from langchain.mcp import MCPAdapter

from client.agent import create_taskpilot_agent
from client.mcp_config import MCP_SERVERS_CONFIG


async def main():

    async with MCPAdapter(MCP_SERVERS_CONFIG) as adapter:

        # Dynamically discover tools from both MCP servers
        tools = await adapter.list_tools()

        print("\nDiscovered tools:")
        for tool in tools:
            print("-", tool.name)

        # Create the TaskPilot agent
        agent = create_taskpilot_agent(tools)

        # Test natural-language task creation
        response = await agent.ainvoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": (
                            "Create a high-priority task "
                            "to prepare the project documentation."
                        ),
                    }
                ]
            }
        )

        print("\nTaskPilot Response:")
        print(response["messages"][-1].content)


if __name__ == "__main__":
    asyncio.run(main())
