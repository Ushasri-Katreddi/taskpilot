
import os

from dotenv import load_dotenv
from langchain_groq import ChatGroq


load_dotenv()


def get_llm() -> ChatGroq:
    """Initialize and return the Groq chat model."""

    api_key = os.getenv("GROQ_API_KEY")
    model_name = os.getenv(
        "GROQ_MODEL",
        "openai/gpt-oss-20b",
    )

    if not api_key:
        raise ValueError(
            "GROQ_API_KEY is missing. Check your .env file."
        )

    return ChatGroq(
        model=model_name,
        temperature=0,
        reasoning_effort="low",
        max_tokens=4096,
        model_kwargs={
            "include_reasoning": False,
        },
        max_retries=2,
        api_key=api_key,
    )
