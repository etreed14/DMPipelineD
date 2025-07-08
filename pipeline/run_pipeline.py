"""
run_pipeline.py — CLI entrypoint to run all 5 stages
"""

import argparse, datetime
from pathlib import Path
from pipeline.llm_calls import LLMClient
from pipeline import formatter
from pipeline.prompts import promptV9c
from pipeline.PromptStages import (
    prompt_stage_a,
    prompt_stage_b,
    prompt_stage_c,
    prompt_stage_d,
    prompt_stage_e,
)

def run_pipeline(input_path: Path, title: str) -> None:
    client = LLMClient()

    # Load transcript
    transcript = input_path.read_text(encoding="utf-8").strip()

    print("🟡 Running Stage A...")
    a_out = prompt_stage_a.run(transcript, client)
    print("🟢 Stage A complete")

    print("🟡 Running Stage B...")
    b_out = prompt_stage_b.run(transcript, client)
    print("🟢 Stage B complete")

    print("🟡 Running Stage C...")
    merged_input = a_out + "\n\n" + b_out
    c_out = prompt_stage_c.run(merged_input, client)
    print("🟢 Stage C complete")

    print("🟡 Running Stage D...")
    d_out = prompt_stage_d.run(c_out, client)
    print("🟢 Stage D complete")

    print("🟡 Running Stage E...")
    e_out = prompt_stage_e.run(d_out, client)
    print("🟢 Stage E complete")

    # Format final HTML
    html = formatter.build_html(title=title, body=e_out)

    # Save output next to input file
    output_path = input_path.with_name(input_path.stem.replace("Transcript", title) + ".html")
    output_path.write_text(html, encoding="utf-8")

    print(f"✅ Done — saved to:\n{output_path.absolute()}")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--file", required=True, help="Path to Din7-8Transcript.txt")
    p.add_argument("--title", required=True, help="Final output title, e.g. SportsBetting")
    args = p.parse_args()
    run_pipeline(Path(args.file), title=args.title)
