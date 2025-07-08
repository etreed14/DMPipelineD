"""
utils.py — helper utilities (transcript compression, etc.)
"""

import re

# Matches "Speaker 5 [12:34:56]" → speaker 5, minute 12
_TIME_RE = re.compile(r"Speaker\s+(\d+)\s+\[(\d{2}):(\d{2}):\d{2}\]")

def compress_transcript(raw: str) -> str:
    """
    Convert a verbose transcript to the compact format:

        • First line in a minute :  5|12 Text …
        • Other lines same min   :  5 Text …

    Lines that don’t match the expected pattern are skipped.
    """
    out, last_min = [], None

    for ln in raw.splitlines():
        match = _TIME_RE.match(ln)
        if not match:
            continue  # skip malformed or empty lines

        speaker, minute, _sec = match.groups()
        minute = int(minute)
        text = ln.split("]", 1)[1].strip()   # drop prefix

        if minute != last_min:
            out.append(f"{speaker}|{minute} {text}")
            last_min = minute
        else:
            out.append(f"{speaker} {text}")

    return "\n".join(out)
