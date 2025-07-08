from ..llm_calls import stage_a
from .. import prompts


def run(transcript: str) -> str:
    return stage_a(prompts.PromptV9a, transcript)
