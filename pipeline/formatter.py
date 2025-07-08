"""
formatter.py — bullet splitter + dark-mode HTML builder
"""

import html
import re
from pathlib import Path

_SPLIT_RE = re.compile(r"\s*(?:;| and | but )\s*", flags=re.I)

def split_bullets(text: str) -> str:
    """
    For each bullet line, if it contains multiple ideas joined by
    ';', ' and ', or ' but ', split into two lines and indent the
    latter with 4 spaces + bullet.
    """
    out = []
    for ln in text.splitlines():
        if any(tok in ln for tok in (" ; ", " and ", " but ")):
            first, rest = _SPLIT_RE.split(ln, 1)
            out.append(first.strip())
            out.append("    • " + rest.strip())
        else:
            out.append(ln.rstrip())
    return "\n".join(out)

# ---------------------------------------------------------------------
# Dark-mode HTML template
# ---------------------------------------------------------------------

_CSS = (
    "body{background:#000;color:#fff;font-family:Arial,sans-serif;"
    "line-height:1.5;padding:40px}"
    "h2.hdr{font-size:22px;font-weight:bold;margin:30px 0 10px}"
    "h2.hdr .ticker{font-size:24px;font-weight:bold;color:#fff}"
    "h2.hdr .rest{font-size:20px;font-weight:normal;color:#fff}"
    "pre{white-space:pre-wrap;font-size:16px}"
)

def build_html(title: str, body: str) -> str:
    """
    Return a full <!DOCTYPE html> document in dark mode.
    Body is escaped to avoid accidental HTML injection.
    """
    safe_body = html.escape(body)
    return (
        "<!DOCTYPE html><html><head><meta charset='utf-8'>"
        f"<title>{html.escape(title)}</title>"
        f"<style>{_CSS}</style></head><body>"
        f"<h1>{html.escape(title)}</h1>\n<pre>{safe_body}</pre>"
        "</body></html>"
    )
