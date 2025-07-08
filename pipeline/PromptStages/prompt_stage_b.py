# prompt_stage_b.py — Stage B (Quick Stats / Fact Ledger)

from pipeline.prompts import promptV9b
from pipeline.llm_calls import LLMClient

def run(transcript_txt: str, client: LLMClient) -> str:
    """
    Run Stage B (Fact Ledger) using promptV9b.
    """
    return client.chat(system_prompt=promptV9b, user_prompt=transcript_txt)
