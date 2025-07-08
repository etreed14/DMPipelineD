# prompt_stage_c.py — Stage C (Merge + Cleaned Summary)

from pipeline.prompts import promptV9c
from pipeline.llm_calls import LLMClient

def run(assembled_summary: str, client: LLMClient) -> str:
    """
    Run Stage C (merge and clean summary) using promptV9c.
    """
    return client.chat(system_prompt=promptV9c, user_prompt=assembled_summary)
