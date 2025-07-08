import time
import os
from pathlib import Path
from .run_pipeline import process_file

IMPORT_DIR = Path('importTranscript')


def watch(directory=IMPORT_DIR):
    print(f"Watching {directory} for new files...")
    processed = set()
    while True:
        for path in directory.iterdir():
            if path.is_file() and path not in processed:
                title = path.stem
                process_file(path, title)
                processed.add(path)
                try:
                    path.unlink()
                except Exception as e:
                    print(f"Could not delete {path}: {e}")
        time.sleep(5)


if __name__ == "__main__":
    watch()
