"""Stage C prompt logic with formatting."""

from ..llm_calls import LLMClient
from ..prompts import PROMPT_V9C
from ..formatter import build_html


def run(summary: str, details: str, client: LLMClient) -> str:
    content = f"{summary}\n\n{details}"
    messages = [
        {"role": "system", "content": PROMPT_V9C},
        {"role": "user", "content": content},
    ]
    result = client.chat(messages)
    return build_html(summary, result)
