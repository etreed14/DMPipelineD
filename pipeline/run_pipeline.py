# run_pipeline.py — Stage A only, with compressed transcript + summary naming

import argparse
from pathlib import Path
from pipeline.llm_calls import LLMClient
from pipeline.prompts import promptV9a
from pipeline.utils import compress_transcript


def to_camel(title: str) -> str:
    """Convert 'sports betting' → 'SportsBetting'"""
    return "".join(word.capitalize() for word in title.strip().split())


def run_pipeline(input_path: Path, title: str) -> None:
    # 1. Load + compress transcript
    raw_text = input_path.read_text(encoding="utf-8")
    transcript = compress_transcript(raw_text)

    # 2. Build file base: e.g., din0709 + SportsBetting
    stem = input_path.stem  # e.g., din0709TranscriptA
    prefix = stem[:7]       # e.g., din0709
    camel_title = generated_title  # use the model's title

    # 3. Save cleaned transcript as din0709TrscptSportsBetting.txt
    cleaned_name = f"{prefix}Trscpt{camel_title}.txt"
    cleaned_path = input_path.with_name(cleaned_name)
    cleaned_path.write_text(transcript, encoding="utf-8")
    print(f"📄 Cleaned transcript saved to: {cleaned_path}")

    # 4. Run Stage A
    client = LLMClient(model="gpt-4o")
    result = client.chat(promptV9a, transcript)
    lines = result.strip().split("\n", 1)
    generated_title = lines[0].strip().replace(" ", "")  # remove extra spaces
    summary = lines[1].strip() if len(lines) > 1 else ""

    # 5. Save plain summary as din0709SportsBetting.html
    summary_name = f"{prefix}{camel_title}.html"
    summary_path = input_path.with_name(summary_name)

    html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>{camel_title}</title></head>
<body><h1>{camel_title}</h1><pre>{result.strip()}</pre></body></html>"""

    summary_path.write_text(html, encoding="utf-8")
    print(f"✅ Summary saved to: {summary_path.resolve()}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file",  required=True, help="Path to transcript .txt file")
    parser.add_argument("--title", required=True, help="Short summary title (e.g. Sports Betting)")
    args = parser.parse_args()
    run_pipeline(Path(args.file), args.title)
