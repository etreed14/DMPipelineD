"""
llm_calls.py — hardened GPT wrapper
"""

import os
import time
import openai
import tiktoken
from openai import RateLimitError, APIError, InvalidRequestError

# ---------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------
DEFAULT_MODEL          = "gpt-3.5-turbo"
MAX_TOKENS_PER_MINUTE  = 30_000
RETRY_STEPS            = (1, 5, 30, 60, 60)   # sec
openai.api_key         = os.getenv("OPENAI_API_KEY")


class LLMClient:
    """
    Shared client with rolling TPM guard, exponential back-off, and
    optional streaming.  Usage:

        client = LLMClient(model="gpt-4o", verbose=True)
        reply  = client.chat(sys_prompt, user_prompt)
    """

    def __init__(self, model: str | None = None, verbose: bool = False):
        self.model   = os.getenv("OPENAI_MODEL", model or DEFAULT_MODEL)
        self.verbose = verbose
        self._enc    = tiktoken.encoding_for_model(self.model)
        self._window_start = time.time()
        self._tokens_used  = 0

    # -------------------- token helpers --------------------
    def _count(self, text: str) -> int:
        return len(self._enc.encode(text))

    # -------------------- tpm guard ------------------------
    def _maybe_pause(self, tokens_needed: int) -> None:
        elapsed = time.time() - self._window_start
        if elapsed > 60:
            self._window_start = time.time()
            self._tokens_used  = 0
            elapsed = 0

        if self._tokens_used + tokens_needed > MAX_TOKENS_PER_MINUTE:
            wait = 60 - elapsed
            if self.verbose:
                print(f"⏳ Throttling {wait:.1f}s to stay < {MAX_TOKENS_PER_MINUTE} TPM")
            time.sleep(wait)
            self._window_start = time.time()
            self._tokens_used  = 0

    def _record(self, n: int) -> None:
        self._tokens_used += n

    # -------------------- main call ------------------------
    def chat(
        self,
        system_prompt: str,
        user_prompt: str,
        stream: bool = False,
    ) -> str:
        in_tokens  = self._count(system_prompt) + self._count(user_prompt)
        out_budget = 3_000                                  # generous
        self._maybe_pause(in_tokens + out_budget)

        messages = [
            {"role": "system", "content": "You are MtgGPT."},
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_prompt},
        ]

        for attempt, delay in enumerate(RETRY_STEPS):
            try:
                rsp = openai.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=0.3,
                    stream=stream,
                )
                break
            except (RateLimitError, APIError) as e:
                if attempt == len(RETRY_STEPS) - 1:
                    raise
                if self.verbose:
                    print(f"⚠️ {type(e).__name__} — retrying in {delay}s")
                time.sleep(delay)
            except InvalidRequestError as e:
                # Context-length exceeded → bubble up with nicer msg
                if "context_length" in str(e):
                    raise RuntimeError(
                        "🛑 Input too large for model context window. "
                        "Consider further transcript compression."
                    ) from e
                raise

        # -------------------- collect output --------------------
        if stream:
            chunks, result_text = [], ""
            for chunk in rsp:
                delta = chunk.choices[0].delta.content or ""
                chunks.append(delta)
            result_text = "".join(chunks).strip()
        else:
            result_text = rsp.choices[0].message.content.strip()

        self._record(in_tokens + self._count(result_text))
        if self.verbose:
            print(f"✅ {self.model}: {in_tokens}→{self._count(result_text)} tokens")
        return result_text
