from ..llm_calls import stage_c
from .. import prompts


def run(stage_a_result: str, stage_b_result: str) -> str:
    return stage_c(prompts.PromptV9c, stage_a_result, stage_b_result)
