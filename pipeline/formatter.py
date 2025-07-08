"""Utilities for formatting LLM output and building HTML."""

from __future__ import annotations

from typing import Tuple


def split_stage_a(text: str) -> Tuple[str, str]:
    """Dummy splitter for stage A output."""
    parts = text.split("\n", 1)
    return parts[0], parts[1] if len(parts) > 1 else ""


def build_html(summary: str, details: str) -> str:
    """Build simple HTML from summary and details."""
    return f"<h1>{summary}</h1><p>{details}</p>"
