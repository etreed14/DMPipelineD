"""
run_pipeline.py — CLI entrypoint (GPT-3.5-turbo edition)

Usage:
    python -m pipeline.run_pipeline \
        --file Calls/2025/July/08/Din7-8Transcript.txt \
        --title SportsBetting
"""

import argparse
from pathlib import Path
from pipeline.llm_calls import LLMClient
from pipeline import formatter
from pipeline.PromptStages import (
    prompt_stage_a,
    prompt_stage_b,
    prompt_stage_c,
    prompt_stage_d,
    prompt_stage_e,
)


def run_pipeline(input_path: Path, title: str) -> None:
    # --- 1 · Load transcript -------------------------------------------------
    transcript = input_path.read_text(encoding="utf-8").strip()

    # --- 2 · Shared LLM client (GPT-3.5-turbo) -------------------------------
    client = LLMClient(model="gpt-3.5-turbo")

    # --- 3 · Run Stages A-E --------------------------------------------------
    print("🟡 Stage A …")
    a_out = prompt_stage_a.run(transcript, client)
    print("🟢 Stage A ✔\n")

    print("🟡 Stage B …")
    b_out = prompt_stage_b.run(transcript, client)
    print("🟢 Stage B ✔\n")

    print("🟡 Stage C …")
    merged_input = f"{a_out}\n\n{b_out}"
    c_out = prompt_stage_c.run(merged_input, client)
    print("🟢 Stage C ✔\n")

    print("🟡 Stage D …")
    d_out = prompt_stage_d.run(c_out, client)
    print("🟢 Stage D ✔\n")

    print("🟡 Stage E …")
    e_out = prompt_stage_e.run(d_out, client)
    print("🟢 Stage E ✔\n")

    # --- 4 · Build & save HTML ----------------------------------------------
    html = formatter.build_html(title=title, body=e_out)
    output_path = input_path.with_name(
        input_path.stem.replace("Transcript", title) + ".html"
    )
    output_path.write_text(html, encoding="utf-8")

    print(f"✅ Pipeline complete — HTML saved to:\n{output_path.resolve()}")


if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--file", required=True, help="Din7-8Transcript.txt path")
    p.add_argument("--title", required=True, help="Meeting title (e.g. SportsBetting)")
    args = p.parse_args()
    run_pipeline(Path(args.file), args.title)
