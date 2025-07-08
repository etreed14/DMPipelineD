from ..llm_calls import stage_b
from .. import prompts


def run(transcript: str) -> str:
    return stage_b(prompts.PromptV9b, transcript)
