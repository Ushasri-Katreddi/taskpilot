
from langchain.agents.middleware import wrap_tool_call
from langchain.messages import ToolMessage


@wrap_tool_call
async def handle_tool_errors(request, handler):
    """Catch tool execution errors and return them to the agent."""

    try:
        return await handler(request)

    except Exception as error:
        tool_name = request.tool_call["name"]

        print(f"\n[TOOL ERROR] {tool_name}: {error}")

        return ToolMessage(
            content=(
                f"The tool '{tool_name}' failed. "
                f"Error details: {str(error)}. "
                "Explain the issue to the user clearly. "
                "Do not claim the operation succeeded."
            ),
            tool_call_id=request.tool_call["id"],
        )
