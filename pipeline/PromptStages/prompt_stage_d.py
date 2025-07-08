# prompt_stage_d.py — Stage D (Coverage & Completeness Patch)

from pipeline.prompts import promptV9d
from pipeline.llm_calls import LLMClient

def run(stage_c_output: str, client: LLMClient) -> str:
    """
    Run Stage D (patch missing companies or facts) using promptV9d.
    """
    return client.chat(system_prompt=promptV9d, user_prompt=stage_c_output)
