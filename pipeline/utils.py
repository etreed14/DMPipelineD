import re

# Match both styles:
# 1. Speaker 3 [01:23:45]
# 2. Unknown Speaker  1:23 or 12:15 or 1:02:33
SPEAKER_LINE_RE = re.compile(r"^(Speaker \d+|Unknown Speaker)[\s\[]+((\d+:)?\d{1,2}):\d{2}")

def compress_transcript(raw: str) -> str:
    """
    Converts raw transcript lines into compressed format:
        • 3|23 text... (first line in a minute)
        • 3    text... (same speaker + minute)
    Supports both bracketed and plain speaker/time formats.
    """
    out = []
    current_speaker = None
    current_minute = None
    lines = raw.splitlines()

    for line in lines:
        line = line.strip()

        # Check for speaker + timestamp pattern
        match = SPEAKER_LINE_RE.match(line)
        if match:
            speaker_raw, timestamp = match.group(1), match.group(2)
            minute = extract_minute(timestamp)
            speaker = speaker_raw.replace("Unknown Speaker", "0").replace("Speaker ", "")
            current_speaker = speaker
            current_minute = minute
            continue  # skip speaker label lines

        # Skip if we have no speaker/minute context yet
        if not line or current_speaker is None or current_minute is None:
            continue

        prefix = f"{current_speaker}|{current_minute}" if is_new_minute(out, current_speaker, current_minute) else current_speaker
        out.append(f"{prefix} {line}")

    return "\n".join(out)

def extract_minute(timestamp: str) -> int:
    """Extracts minute from HH:MM:SS or MM:SS"""
    parts = list(map(int, timestamp.split(":")))
    if len(parts) == 3: return parts[1]     # HH:MM:SS → return MM
    if len(parts) == 2: return parts[0]     # MM:SS → return MM
    return 0

def is_new_minute(out: list[str], speaker: str, minute: int) -> bool:
    """Returns True if this line is the first for that speaker+minute block"""
    if not out: return True
    return not out[-1].startswith(f"{speaker}|{minute}")
