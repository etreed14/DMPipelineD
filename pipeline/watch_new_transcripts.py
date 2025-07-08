"""Watch the importTranscript folder for new files and process them."""

from __future__ import annotations

import time
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from .run_pipeline import process_file


class Handler(FileSystemEventHandler):
    def on_created(self, event):
        path = Path(event.src_path)
        if path.suffix == ".txt":
            process_file(path, title=path.stem)


def watch(folder: Path) -> None:
    observer = Observer()
    handler = Handler()
    observer.schedule(handler, str(folder), recursive=False)
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


if __name__ == "__main__":
    watch(Path("importTranscript"))
