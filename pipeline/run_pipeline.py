"""Command line interface for processing a single transcript file."""

from __future__ import annotations

import argparse
from pathlib import Path

from .llm_calls import LLMClient
from .PromptStages import prompt_stage_a, prompt_stage_b, prompt_stage_c
from .formatter import split_stage_a


def process_file(path: Path, title: str) -> str:
    client = LLMClient()
    text = path.read_text()
    stage_a_output = prompt_stage_a.run(text, client)
    summary, details = split_stage_a(stage_a_output)
    stage_b_output = prompt_stage_b.run(text, client)
    html = prompt_stage_c.run(summary, stage_b_output, client)
    return html


def main() -> None:
    parser = argparse.ArgumentParser(description="Run meeting summary pipeline")
    parser.add_argument("--file", type=Path, required=True)
    parser.add_argument("--title", default="Meeting")
    args = parser.parse_args()

    html = process_file(args.file, args.title)
    output_path = Path("Calls") / f"{args.file.stem}.html"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html)
    print(f"Wrote {output_path}")


if __name__ == "__main__":
    main()
