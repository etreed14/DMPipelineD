PROMPT_V9A = r"""
IGNORE ALL EARLIER CHATS.

Your task has two parts:

1. Return a short 1–3 word CamelCase title that best describes the main investment theme(s) discussed in the transcript. Put it on the first line by itself.

2. Then output a clean investor-style bullet summary for each company discussed.

Instructions for summary:
• Begin each company section with: **(TICKER) — Long / Short — mm/dd/yyyy — $price**
• Use clean bullet formatting (not prose)
• If a line has multiple ideas, split into sub-bullets
• Push numbers and dates into indented lines

Output format:
Title line (CamelCase)
---
• Summary bullets
...
"""

# lowercase aliases expected by other modules
promptV9a = PROMPT_V9A
# promptV9b = PROMPT_V9B
# promptV9c = PROMPT_V9C
# promptV9d = PROMPT_V9D
# promptV9e = PROMPT_V9E
