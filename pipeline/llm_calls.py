"""OpenAI API wrapper with basic retry logic."""

from __future__ import annotations

import os
import time
from typing import Any, Dict

import openai


class LLMClient:
    """Simple OpenAI API client with rate limiting and retries."""

    def __init__(self, api_key: str | None = None, model: str | None = None):
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY not provided")
        self.model = model or "gpt-3.5-turbo"
        openai.api_key = self.api_key

    def chat(self, messages: list[Dict[str, str]], max_retries: int = 3) -> str:
        """Send chat completion request with retries."""
        for attempt in range(max_retries):
            try:
                response = openai.ChatCompletion.create(model=self.model, messages=messages)
                return response["choices"][0]["message"]["content"]
            except openai.error.RateLimitError:
                if attempt == max_retries - 1:
                    raise
                time.sleep(2 ** attempt)
        raise RuntimeError("Failed to get response from OpenAI")
