"""
llm_calls.py — GPT interface with retry + token guard
"""

import os, time
import openai
from openai import RateLimitError, APIError

openai.api_key = os.getenv("OPENAI_API_KEY")

DEFAULT_MODEL = "gpt-4o"
MAX_TOKENS_PER_MINUTE = 30_000

class LLMClient:
    def __init__(self, model: str = DEFAULT_MODEL):
        self.model = model
        self._window_start = time.time()
        self._tokens_used = 0

    def _maybe_pause(self, tokens_needed: int):
        elapsed = time.time() - self._window_start
        if elapsed > 60:
            self._window_start = time.time()
            self._tokens_used = 0
            return
        if self._tokens_used + tokens_needed > MAX_TOKENS_PER_MINUTE:
            wait_time = 60 - elapsed
            print(f"⏳ Throttling — waiting {wait_time:.1f}s to stay under token limit")
            time.sleep(wait_time)
            self._window_start = time.time()
            self._tokens_used = 0

    def _record_tokens(self, n: int):
        self._tokens_used += n

    def chat(self, system_prompt: str, user_prompt: str) -> str:
        est_in = (len(system_prompt) + len(user_prompt)) // 4
        est_out = 3000
        self._maybe_pause(est_in + est_out)

        for attempt in range(3):
            try:
                response = openai.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    temperature=0.3
                )
                break
            except (RateLimitError, APIError) as e:
                if attempt == 2:
                    raise
                print("⚠️ OpenAI retry in 60s due to:", str(e))
                time.sleep(60)

        out = response.choices[0].message.content.strip()
        self._record_tokens(est_in + len(out) // 4)
        return out
