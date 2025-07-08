"""
formatter.py — bullet splitter + HTML builder
"""

import html

def split_bullets(stage_a_text: str) -> str:
    """
    Split multi-idea Stage A bullets using ; / and / but
    and indent supporting lines under the first.
    """
    out = []
    for line in stage_a_text.splitlines():
        if " ; " in line or " and " in line or " but " in line:
            parts = line.strip().split(" ; ")
            if len(parts) == 1:
                parts = line.strip().split(" and ")
            if len(parts) == 1:
                parts = line.strip().split(" but ")
            out.append(parts[0].strip())
            for sub in parts[1:]:
                out.append("    • " + sub.strip())
        else:
            out.append(line.strip())
    return "\n".join(out)

def build_html(title: str, body: str) -> str:
    """
    Wrap the merged summary (Stage E output) in dark HTML.
    """
    safe_body = html.escape(body)
    styled_body = safe_body.replace("\n", "<br>\n")  # preserve line breaks
    return f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8">
<style>
  body {{
    background:#000;
    color:#fff;
    font-family:Arial,sans-serif;
    line-height:1.5;
    padding:40px;
  }}
  h2.hdr {{
    font-size:22px;
    font-weight:bold;
    margin:30px 0 10px;
  }}
  .ticker {{
    font-size:24px;
    font-weight:bold;
    color:#fff;
  }}
  .rest {{
    font-size:20px;
    font-weight:normal;
    color:#fff;
  }}
</style>
<title>{title}</title>
</head>
<body>{styled_body}</body></html>
"""
