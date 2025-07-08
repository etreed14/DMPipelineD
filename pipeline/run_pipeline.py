"""
run_pipeline.py — CLI entry-point (GPT-3.5-turbo, with transcript compression)

Example:
    python -m pipeline.run_pipeline \
        --file Calls/2025/July/08/Din7-8Transcript.txt \
        --title SportsBetting
"""

import argparse
from pathlib import Path

from pipeline.llm_calls import LLMClient
from pipeline import formatter
from pipeline.utils import compress_transcript  # ← NEW

from pipeline.PromptStages import (
    prompt_stage_a,
    prompt_stage_b,
    prompt_stage_c,
    prompt_stage_d,
    prompt_stage_e,
)


def process_file(input_path: Path, title: str) -> str:
    """Simplified pipeline used for unit tests."""
    client = LLMClient(model="gpt-4o")
    text = input_path.read_text()
    result = client.chat("You are an analyst.", text)  # ✅ 2 arguments now
    parts = result.split("\n", 1)
    summary = parts[0]
    details = parts[1] if len(parts) > 1 else ""
    return f"<h1>{summary}</h1><p>{details}</p>"


def run_pipeline(input_path: Path, title: str) -> None:
    from pipeline.utils import compress_transcript
    transcript = compress_transcript(input_path.read_text(encoding="utf-8"))
    client = LLMClient(model="gpt-4o")

    print("🟡 Stage A …")
    a_out = prompt_stage_a.run(transcript, client)
    print("🟢 Stage A ✔")

    print("🟡 Stage B …")
    b_out = prompt_stage_b.run(transcript, client)
    print("🟢 Stage B ✔")

    merged = f"### STAGE A ###\n{a_out.strip()}\n\n### STAGE B ###\n{b_out.strip()}"

    print("🟡 Stage C …")
    c_out = prompt_stage_c.run(merged, client)
    print("🟢 Stage C ✔")

    print("🟡 Stage D …")
    d_out = prompt_stage_d.run(c_out, client)
    print("🟢 Stage D ✔")

    print("🟡 Stage E …")
    e_out = prompt_stage_e.run(d_out, client)
    print("🟢 Stage E ✔")

    html = formatter.build_html(title=title, body=e_out)
    output_path = input_path.with_name(input_path.stem.replace("Transcript", title) + ".html")
    output_path.write_text(html, encoding="utf-8")
    print(f"✅ Pipeline complete — HTML saved to:\n{output_path.resolve()}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file",  required=True, help="Path to Din7-8Transcript.txt")
    parser.add_argument("--title", required=True, help="Meeting title (e.g. SportsBetting)")
    args = parser.parse_args()
    run_pipeline(Path(args.file), args.title)
