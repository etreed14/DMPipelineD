import argparse
from pathlib import Path
import shutil
from datetime import datetime
from . import stages, prompts
from .llm_calls import stage_a, stage_b, stage_c

CALLS_DIR = Path('Calls')
WORKING_DIR = Path('pipeline/working')
HTML_TEMPLATE = Path('pipeline/html/template_dark.html')


def save_html(content: str, title: str, call_date: datetime):
    dest_dir = CALLS_DIR / call_date.strftime('%Y') / call_date.strftime('%B') / call_date.strftime('%d')
    dest_dir.mkdir(parents=True, exist_ok=True)
    html_name = f"Din7-8{title}.html"
    dest_file = dest_dir / html_name
    dest_file.write_text(content, encoding='utf-8')
    print(f"Saved {dest_file}")
    return dest_file


def process_file(path: Path, title: str):
    call_date = datetime.now()
    dest_dir = CALLS_DIR / call_date.strftime('%Y') / call_date.strftime('%B') / call_date.strftime('%d')
    dest_dir.mkdir(parents=True, exist_ok=True)
    text_dest = dest_dir / f"Din7-8Transcript.txt"
    text_dest.write_text(path.read_text(encoding='utf-8'), encoding='utf-8')

    transcript = text_dest.read_text(encoding='utf-8')
    stage_a_result = stage_a(prompts.PromptV9a, transcript)
    stage_b_result = stage_b(prompts.PromptV9b, transcript)
    html_content = stage_c(prompts.PromptV9c, stage_a_result, stage_b_result)

    html_path = save_html(html_content, title, call_date)
    return html_path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', required=True)
    parser.add_argument('--title', required=True)
    args = parser.parse_args()
    process_file(Path(args.file), args.title)


if __name__ == '__main__':
    main()
