# prompt_stage_e.py — Stage E (Insert Price & Earnings Dates)

from pipeline.prompts import promptV9e
from pipeline.llm_calls import LLMClient

def run(patched_summary: str, client: LLMClient) -> str:
    """
    Run Stage E (insert price and earnings) using promptV9e.
    """
    return client.chat(system_prompt=promptV9e, user_prompt=patched_summary)
