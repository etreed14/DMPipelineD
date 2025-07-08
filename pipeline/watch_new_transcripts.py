"""
watch_new_transcripts.py — drop-box watcher

Run:
    python -m pipeline.watch_new_transcripts
Ctrl-C to stop.
"""

import shutil, time, datetime
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events   import FileSystemEventHandler

from pipeline.run_pipeline import run_pipeline

INBOX   = Path("importTranscript")
ARCHIVE = Path("Calls")

class Handler(FileSystemEventHandler):
    def on_created(self, event):
        fp = Path(event.src_path)
        if fp.is_dir() or fp.suffix.lower() != ".txt":
            return

        # Date folders = today (adjust if your filenames encode a date)
        today = datetime.date.today()
        dest_dir = ARCHIVE / f"{today.year}" / today.strftime("%B") / f"{today.day:02}"
        dest_dir.mkdir(parents=True, exist_ok=True)

        dest_name = f"Din{today.month}-{today.day}Transcript.txt"
        dest_path = dest_dir / dest_name
        shutil.move(fp, dest_path)
        print(f"📥 Moved → {dest_path}")

        # Run pipeline — use filename stem (minus 'Transcript') as title placeholder
        run_pipeline(dest_path, title="Summary")

if __name__ == "__main__":
    INBOX.mkdir(exist_ok=True)
    obs = Observer()
    obs.schedule(Handler(), INBOX, recursive=False)
    obs.start()
    print("👀 Watching importTranscript/  (Ctrl-C to stop)")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        obs.stop()
    obs.join()
