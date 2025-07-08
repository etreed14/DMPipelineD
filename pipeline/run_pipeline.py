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


def run_pipeline(input_path: Path, title: str) -> None:
    # ── 1 · Load + compress transcript ────────────────────────────────────
    raw_txt = input_path.read_text(encoding="utf-8")
    transcript = compress_transcript(raw_txt)

    # ── 2 · Shared LLM client (GPT-3.5-turbo) ─────────────────────────────
    client = LLMClient(model="gpt-3.5-turbo")

    # ── 3 · Run Stages A-E ────────────────────────────────────────────────
    print("🟡 Stage A …")
    a_out = prompt_stage_a.run(transcript, client)
    print("🟢 Stage A ✔\n")

    print("🟡 Stage B …")
    b_out = prompt_stage_b.run(transcript, client)
    print("🟢 Stage B ✔\n")

    # Delimiters help Stage C align bullets accurately
    merged_input = (
        "### STAGE A ###\n" + a_out.strip() +
        "\n\n### STAGE B ###\n" + b_out.strip()
    )

    print("🟡 Stage C …")
    c_out = prompt_stage_c.run(merged_input, client)
    print("🟢 Stage C ✔\n")

    print("🟡 Stage D …")
    d_out = prompt_stage_d.run(c_out, client)
    print("🟢 Stage D ✔\n")

    print("🟡 Stage E …")
    e_out = prompt_stage_e.run(d_out, client)
    print("🟢 Stage E ✔\n")

    # ── 4 · Build & save dark-mode HTML ───────────────────────────────────
    html = formatter.build_html(title=title, body=e_out)
    output_path = input_path.with_name(
        input_path.stem.replace("Transcript", title) + ".html"
    )
    output_path.write_text(html, encoding="utf-8")

    print(f"✅ Pipeline complete — HTML saved to:\n{output_path.resolve()}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file",  required=True, help="Path to Din7-8Transcript.txt")
    parser.add_argument("--title", required=True, help="Meeting title (e.g. SportsBetting)")
    args = parser.parse_args()
    run_pipeline(Path(args.file), args.title)
