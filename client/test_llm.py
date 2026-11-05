import asyncio
from client.llm import get_llm


async def main():
    llm = get_llm()

    response = await llm.ainvoke(
        "In the context of AI applications, explain what "
        "an MCP server does in exactly two sentences."
    )

    print("\nModel:", response.response_metadata.get("model_name"))
    print("Answer:", response.content)
    print("Usage:", response.usage_metadata)


if __name__ == "__main__":
    asyncio.run(main())