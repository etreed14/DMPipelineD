PROMPT_V9A = r"""
IGNORE ALL EARLIER CHATS.  
Your only job is to generate a clean, bullet-point summary for each company mentioned in the transcript.

Instructions:
• Start with a header line: **(TICKER) — Long / Short — mm/dd/yyyy — $price**
• Then write investor-style bullets for catalysts, valuation, risks, etc.
• Use natural bullet phrasing (not prose).
• If a line contains multiple ideas, split it into separate bullets.
• Indent supporting bullets below their parent (1 level only).
• Push all figures (%, $, dates) to sub-bullets.

Output just the summary. No commentary. No disclaimers. No metadata.
"""

# Alias for compatibility
promptV9a = PROMPT_V9A
