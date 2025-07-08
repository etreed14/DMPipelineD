"""Prompt templates for the meeting-summary pipeline (v9)."""

# ── Stage A prompt ───────────────────────────────────────────
PROMPT_V9A = r"""
##### MtgGPTPrompt v9  (clean A + Quick Stats B) #####
IGNORE ALL EARLIER CHATS.  THIS FILE IS YOUR ONLY INSTRUCTION SET.

You will always receive exactly two plaintext files:
  1️⃣  This prompt file (MtgGPTPromptV9.txt)
  2️⃣  One meeting transcript (e.g. dinnerTranscript.txt)

Run the following three‑stage workflow and STOP.
Exactly 5 pauses are allowed:
  • After Stage A  ➜  === END STAGE A (type "y" to continue) ===
  • After Stage B  ➜  === END STAGE B (type "y" to append stats) ===
  • After Stage C  ➜  === END STAGE C (type "y" for coverage and completeness check) ===
  • After Stage D  ➜  === END STAGE C (type "y" to research & insert comp. data) ===
  • After Stage E  ➜  === END STAGE C (type "y" to finalize and display) ===

────────────────────────────────────────────────────────────
STAGE A — NARRATIVE SUMMARY (clean bullets)
────────────────────────────────────────────────────────────
Goal: craft a fluent, investor‑style pitch for **each company**, NOTHING left out.

Header line (bold):
  **(TICKER) — Long / Short — mm/dd/yyyy — $price**

• Keep adding primary bullets until EVERY material idea is voiced
  (edge, catalysts, valuation maths, debate, risks, colour).  
• One idea per bullet; natural prose.  
• If a bullet contains multiple ideas (joined by “;”, “ and ”, or “ but ”), split into
  separate bullets. Indent new bullet one level.
• Push ALL numbers / % / $ / dates to indented sub‑bullets.

Print every company’s section, then:
=== END STAGE A (type "y" to continue) ===
"""

# ── Stage B prompt ───────────────────────────────────────────
PROMPT_V9B = r"""
##### MtgGPTPrompt v9b Quick Stats B #####
IGNORE ALL EARLIER CHATS.  THIS FILE IS YOUR ONLY INSTRUCTION SET.

────────────────────────────────────────────────────────────
STAGE B — FACT LEDGER (Quick‑stats source)
────────────────────────────────────────────────────────────
Goal: capture **all** stats / metrics / quotes, grouped by company, NONE left out.

Loop over every ticker seen in Stage A:

  (TICKER) — Quick Stats / Metrics
  ──────────────────────
  • Create whatever buckets/bullet headers are needed (Financials & Metrics, Edge/Tech, AI Use Cases, Valuation Anchors, …).
  • Unlimited bullet nesting — NOTHING is dropped.
  • Add buckets and subpoints until everything in transcript is covered
  • Do *not* rewrite or merge with Stage A.

Print every company’s section, then after the final company:
=== END STAGE B (type "y" to merge stats) ===
"""

# ── Stage C prompt ───────────────────────────────────────────
PROMPT_V9C = r"""
##### MtgGPTPrompt v9c — Stage C (Merge & Structure Final Output) #####
IGNORE ALL EARLIER CHATS. THIS FILE IS YOUR ONLY INSTRUCTION SET.

────────────────────────────────────────────────────────────
STAGE C — MERGE & CLEAN FINAL OUTPUT (no redundancy)
────────────────────────────────────────────────────────────

Your goal is to produce a **clean, merged company summary**, combining Stage A and Stage B **without any loss of information** and avoiding redundant restatement.

For each company:

1. **Split + Clean Stage A**
   • Go bullet by bullet through Stage A.
   • If any bullet includes multiple ideas (joined by “;”, “ and ”, or “ but”), split into separate bullets.
   • Indent dependent or supporting ideas one level below.

2. **Attach Stage B facts**
   • Loop through every bullet (or nested line) from Stage B.
   • For each:
     – Match it to the best-fit Stage A bullet using keyword similarity and content.
     – Insert it **as a sub-bullet** under the relevant A-line.
     – Preserve B’s indentation level where helpful (e.g. buckets like Financials).
     – NEVER drop or reword anything from B before this step.

3. **Redundancy Cleanup**
   • After attaching all B-lines, scan for nearby **duplicate** or **near-duplicate** lines.
   • If two lines say nearly the same thing:
     – Keep the clearer / more concise version.
     – If one adds extra detail, **trim the redundant part** and **nest the unique part as a sub-bullet**.
   • Do NOT allow repeated points with different phrasings to remain back-to-back.

4. **Final Structure**
   • Print the cleaned result in plain bullet format.
   • Do NOT include a separate “Quick Stats” section.
   • Do NOT output unused Stage B lines — all must be merged under Stage A bullets.

After all companies:

• DO NOT save or wrap in HTML.
• DO NOT output download links.
• Just print the clean merged summary as text and stop.

STOP after printing the final result.
"""

# ── Stage D prompt ───────────────────────────────────────────
PROMPT_V9D = r"""
##### MtgGPTPrompt v9d — Coverage and Completeness Check (Stage D)
IGNORE ALL EARLIER CHATS. THIS FILE IS YOUR ONLY INSTRUCTION SET.

────────────────────────────────────────────────────────────
STAGE D — VERIFY MERGED COVERAGE & COMPLETENESS
────────────────────────────────────────────────────────────
Goal: Confirm that the Stage C summary is complete and fully merged.
Ensure that:
• Every company mentioned in the transcript has a full summary block.
• Every Stage B bullet has been integrated into the cleaned Stage A bullet tree.

────────────────────────────────────────────
STEP 1 — COMPANY COVERAGE CHECK
────────────────────────────────────────────
• Re-scan the full transcript and the original Stage B output to detect all companies mentioned (by name or ticker).
• Compare that list against the companies included in Stage C.
• If any company is missing from Stage C:
   – Append a new summary section for that company to the end of the output.
   – Use that company’s original Stage A and Stage B outputs.
   – Perform Stage C logic:
     ▪ Split and indent Stage A bullets as needed.
     ▪ Insert Stage B facts under the most relevant Stage A bullet.
     ▪ Preserve all formatting and structure.
• Do NOT drop or summarize any company.

────────────────────────────────────────────
STEP 2 — FACT COMPLETENESS CHECK
────────────────────────────────────────────
• For each company already present in Stage C:
   – Re-compare the Stage C result to the full original Stage B block.
   – Confirm that every Stage B bullet or sub-point has been fully integrated.
• If any B point is missing:
   – Insert it beneath the most relevant Stage A bullet.
   – If a partial overlap exists, remove the redundant portion and preserve the rest.
   – If no match is clear, place the item at the bottom of the section under an indented bullet labeled “Additional Stats”.
• Use the exact wording and structure from Stage B.
• Do NOT drop or paraphrase any Stage B facts. Use them all.

────────────────────────────────────────────
STEP 3 — FINAL OUTPUT
────────────────────────────────────────────
• Print the final merged and patched summary.
• Do NOT rebuild Stage C from scratch — only fill in what’s missing.
• Preserve all formatting, indentation, and bullet style.
• If the original was in dark-mode HTML, retain it.

STOP after printing the updated summary. Do NOT save to file.
"""

# ── Stage E prompt ───────────────────────────────────────────
PROMPT_V9E = r"""
##### MtgGPTPrompt v9e — Stage E (Price & Earnings Insertion)
IGNORE ALL EARLIER CHATS. THIS FILE IS YOUR ONLY INSTRUCTION SET.

────────────────────────────────────────────────────────────
STAGE E — FINAL INSERTIONS: Share Price & Earnings Date
────────────────────────────────────────────────────────────
Goal: For each company block in the final Stage C summary:

1. Replace the placeholders:
   • Replace `$[PRICE]` with the exact **historical closing share price** on the date of the meeting (e.g. July 1, 2025)
   • Replace `Next Earnings Date – [TO BE FILLED IN LATER]` with the actual **next earnings report date**

2. Use live data search to retrieve each value:
   • For share price:
     Search → `"TDC historical close on July 1 2025 site:yahoo.com"`
   • For earnings date:
     Search → `"TDC next earnings date site:nextearningsdate.com"`

3. Insert the values using **official source format**:
   • Share price → exact dollar format (e.g. `$22.46`)
   • Earnings date → full date format (e.g. `August 5, 2025`)

4. Do NOT:
   • Estimate or approximate any value
   • Alter formatting, indentation, or bullet content
   • Add commentary, notes, or explanations
   • Drop companies or skip placeholders

5. If any lookup fails:
   • Leave the original placeholder as-is (`$[PRICE]` or `[TO BE FILLED IN LATER]`)

6. Final step:
   • Print the full summary again with values filled in wherever possible

DO NOT wrap in HTML.  
DO NOT save to a file.  
DO NOT summarize or comment.  
Just print the updated plain-text result.

STOP after printing the complete, updated summary.
"""

# lowercase aliases expected by prompt_stage_* modules
promptV9a = PROMPT_V9A
promptV9b = PROMPT_V9B
promptV9c = PROMPT_V9C
promptV9d = PROMPT_V9D
promptV9e = PROMPT_V9E
