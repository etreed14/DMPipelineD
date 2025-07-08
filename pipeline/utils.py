"""
utils.py — helper utilities (transcript compression, etc.)
"""

import re

# Pattern:  Speaker 5 [12:34:56] The company is ...
_TIME_RE = re.compile(r"Speaker\s+(\d+)\s+\[(\d{2}):(\d{2}):\d{2}\]")

def compress_transcript(raw: str) -> str:
    """
    Convert a verbose transcript to the compact format:
        • First line of a minute :  5|12 Text …
        • Other lines same min   :  5 Text …
    Blank or malformed lines are skipped entirely.
    """
    out, last_min = [], None

    for ln in raw.splitlines():
        match = _TIME_RE.match(ln)
        if not match:
            continue  # ignore lines that don't match "Speaker N [MM:SS:HH]"
        speaker, mm, _ss = match.groups()
        minute = int(mm)
        text = ln.split("]", 1)[1].strip()  # everything after the ]

        if minute != last_min:
            out.append(f"{speaker}|{minute} {text}")
            last_min = minute
        else:
            out.append(f"{speaker} {text}")

    return "\n".join(out)
