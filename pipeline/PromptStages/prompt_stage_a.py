# prompt_stage_a.py — Stage A (Narrative Summary)

from pipeline.prompts import promptV9a
from pipeline.llm_calls import LLMClient

def run(transcript_txt: str, client: LLMClient) -> str:
    """
    Run Stage A (Narrative Summary) using promptV9a.
    """
    return client.chat(system_prompt=promptV9a, user_prompt=transcript_txt)
