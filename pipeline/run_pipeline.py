# run_pipeline.py — Stage A only, auto-title, two-file output

import argparse
from pathlib import Path
from pipeline.llm_calls import LLMClient
from pipeline.prompts import promptV9a
from pipeline.utils import compress_transcript


def run_pipeline(input_path: Path, _ignored_title: str) -> None:
    # 1. Load + compress transcript
    raw_text = input_path.read_text(encoding="utf-8")
    transcript = compress_transcript(raw_text)

    # 2. Run Stage A — expect title + summary
    client = LLMClient(model="gpt-4o")
    result = client.chat(promptV9a, transcript)

    lines = result.strip().split("\n", 1)
    if len(lines) < 2:
        raise ValueError("Model output did not include both title and summary.")
    generated_title, summary = lines
    generated_title = generated_title.strip().replace(" ", "")
    print(f"🏷️  Model-generated title: {generated_title}")

    # 3. Build filename base from original prefix + title
    prefix = input_path.stem[:7]  # e.g. din0709
    base = f"{prefix}{generated_title}"

    # 4. Save compressed transcript
    transcript_path = input_path.with_name(f"{prefix}Trscpt{generated_title}.txt")
    transcript_path.write_text(transcript, encoding="utf-8")
    print(f"📄 Compressed transcript → {transcript_path}")

    # 5. Save light-mode HTML summary
    summary_path = input_path.with_name(f"{base}.html")
    html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>{generated_title}</title></head>
<body><h1>{generated_title}</h1><pre>{summary.strip()}</pre></body></html>"""
    summary_path.write_text(html, encoding="utf-8")
    print(f"✅ Summary saved → {summary_path.resolve()}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True, help="Path to transcript file")
    parser.add_argument("--title", required=True, help="(ignored now, replaced by model)")
    args = parser.parse_args()
    run_pipeline(Path(args.file), args.title)
