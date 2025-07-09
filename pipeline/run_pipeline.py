# run_pipeline.py — Minimal Stage A-only version (clean HTML + compression)

import argparse
from pathlib import Path

from pipeline.llm_calls import LLMClient
from pipeline.prompts import promptV9a
from pipeline.utils import compress_transcript


def run_pipeline(input_path: Path, title: str) -> None:
    # 1. Load + compress transcript
    raw_text = input_path.read_text(encoding="utf-8")
    transcript = compress_transcript(raw_text)

    # 2. Run Stage A only
    client = LLMClient(model="gpt-4o")
    result = client.chat(promptV9a, transcript)

    # 3. Save clean HTML (light mode, no dark styling)
    html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>{title}</title></head>
<body><h1>{title}</h1><pre>{result.strip()}</pre></body></html>"""

    base = input_path.stem.replace("Transcript", "Sum")
    out_path = input_path.with_name(f"{base}.html")
    out_path.write_text(html, encoding="utf-8")
    print(f"✅ Summary saved to: {out_path.resolve()}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file",  required=True, help="Path to transcript text file")
    parser.add_argument("--title", required=True, help="Title for HTML output")
    args = parser.parse_args()
    run_pipeline(Path(args.file), args.title)
