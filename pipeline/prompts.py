"""Prompt template for the meeting-summary pipeline (Stage A only)."""

PROMPT_V9A = r"""
##### MtgGPTPrompt v9a — Stage A (Narrative Summary) #####
IGNORE ALL EARLIER CHATS. THIS FILE IS YOUR ONLY INSTRUCTION SET.

────────────────────────────────────────────────────────────
STAGE A — NARRATIVE SUMMARY (clean bullets)
────────────────────────────────────────────────────────────
Goal: craft a fluent, investor-style pitch for **each company**, NOTHING left out.

Header line (bold):
  **(TICKER) — Long / Short — mm/dd/yyyy — $price**

• Keep adding primary bullets until EVERY material idea is voiced
  (edge, catalysts, valuation maths, debate, risks, colour).  
• One idea per bullet; natural prose.  
• If a bullet contains multiple ideas (joined by “;”, “ and ”, or “ but ”), split into
  separate bullets. Indent new bullet one level.
• Push ALL numbers / % / $ / dates to indented sub-bullets.

Print every company’s section, then:
=== END STAGE A (type "y" to continue) ===
"""

# Alias for compatibility
promptV9a = PROMPT_V9A
