"""Stage B prompt logic."""

from ..llm_calls import LLMClient
from ..prompts import PROMPT_V9B


def run(text: str, client: LLMClient) -> str:
    messages = [
        {"role": "system", "content": PROMPT_V9B},
        {"role": "user", "content": text},
    ]
    return client.chat(messages)
