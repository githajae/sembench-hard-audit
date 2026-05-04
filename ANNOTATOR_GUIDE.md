# Annotator Guide — How to Run This Audit

> Read time: ~5 minutes. Practical run instructions.

This guide assumes you have already read `INTRODUCTION.md` and
`PROTOCOL.md`. If you haven't, do that first — without the rubric the
ratings are inconsistent and the audit is wasted.

---

## 0. Setup (once)

You should have received a folder that looks like this:

```
human_audit/
├── README.md
├── INTRODUCTION.md
├── PROTOCOL.md
├── ANNOTATOR_GUIDE.md       ← you are here
├── LLM_PROMPT.md
├── tasks/                    ← 120 task pages, already populated
│   ├── manifest.json
│   ├── swebench_verified/
│   ├── scifact/
│   ├── contractnli/
│   └── wdc_products/
├── responses/
│   ├── template.json
│   └── EXAMPLE_filled.json
└── scripts/
```

If `tasks/` is empty or missing, ask the organizer to run
`python scripts/build_tasks.py --seed 20260504` first.

Copy the template once:

```bash
cp responses/template.json responses/<your_name>.json
```

Use a name without spaces (e.g. `responses/jaehyun.json`,
`responses/alice.json`).

---

## 1. Working through the tasks

Each task lives at `tasks/<benchmark>/NN_<operator>_<key>.md` (the
human-readable view) with a sibling `.json` (the LLM-friendly view).

Recommended order: go benchmark by benchmark, all 30 tasks of one
benchmark in one sitting. Domain context carries between tasks of the
same benchmark, and you'll be faster after the first few.

For each task page:

1. **Read the page top to bottom.** The **Key facts** block is the
   only block you strictly need for Q1 and Q2 — it contains the
   inputs, the resolved gold evidence (text, not just ids), and the
   `top_k` for rank tasks. The **Verifier rule** block right below it
   is the contract you are auditing in Q2. The **Policy** block is
   the operator's instructions to the model. Everything in **Other
   fields** is collapsed for reference only.
2. **Decide Q1 (naturalness).** If the page reads like a reasonable
   operator call to a domain-aware practitioner, score 4 or 5. If
   only the framing feels off but the underlying task is legitimate,
   score 3. Score ≤2 means the hardening genuinely broke the task.
3. **Decide Q2 (verifier validity).** Imagine a competent system
   producing a correct answer. Would the verifier accept it? Now
   imagine a wrong answer that is plausibly close. Would the verifier
   reject it? If both yes, **agree**. Otherwise pick the appropriate
   `disagree_*` and write a note.
4. **Append your entry** to your responses file (see schema below).

Pace varies by benchmark — see the time budget in `PROTOCOL.md`.
Plan on 6–8 hours of focused work for the full 120 tasks, ideally
split across two sittings.

---

## 2. Response file schema

Your responses file is a single JSON object that looks like:

```json
{
  "annotator_id": "your_name",
  "started_at": "2026-05-04T10:00:00Z",
  "finished_at": "2026-05-04T14:30:00Z",
  "ratings": {
    "<task_key_from_manifest>": {
      "naturalness": 5,
      "verifier_validity": "agree",
      "confidence": "high",
      "notes": ""
    },
    ...
  }
}
```

- `task_key_from_manifest` is the same string used in
  `tasks/manifest.json` (one entry per task, 120 total). The task page
  shows it at the top under **task_key:**. Copy-paste it verbatim —
  `aggregate.py` will warn if your file uses a key that does not
  appear in the manifest, but it will not auto-correct.
- `naturalness`: integer 1..5.
- `verifier_validity`: one of
  `"agree"`, `"disagree_too_strict"`, `"disagree_too_lax"`,
  `"disagree_other"`.
- `confidence`: `"high"`, `"medium"`, `"low"`. Optional but
  encouraged.
- `notes`: free-text. Required when `verifier_validity` ≠ `"agree"`.

`responses/EXAMPLE_filled.json` shows one fully filled task.

You can fill the file with any text editor or with a small script.
The aggregator validates the file at load time and tells you which
fields are missing or malformed.

---

## 3. Using an LLM as a co-pilot (optional)

If you want a second opinion before you commit to a rating, the
recommended flow is:

1. Open the task page (`.md`) and scan it.
2. Open the matching `.json`.
3. Open `LLM_PROMPT.md` and copy its prompt into your favourite chat
   model (Claude, GPT-4, Gemini, …). Paste the task `.json` where
   the prompt asks.
4. Read the model's answer **as a hint, not as truth.** The prompt
   asks the model to reason step by step before giving a rating, so
   you can see *why* it would score the task one way.
5. Make your own decision. Disagreements between you and the LLM are
   useful — they often surface exactly the kinds of edge cases the
   audit is meant to catch.

**Important:** do not just paste the LLM's JSON output as your
answer. The whole point of the audit is to capture *informed human*
judgment. An audit that is 100% LLM is, at best, a model-vs-model
agreement check.

---

## 4. When you're done

1. Save your responses file under `responses/<your_name>.json`.
2. Send the file back to the organizer. (The folder you received
   should not be modified other than by writing this one file.)
3. The organizer runs `python scripts/aggregate.py` once they have
   at least two annotator files, then writes
   `results/summary.md`.

---

## 5. FAQ

**Q. The task page has fields I don't recognize.**

The fields come from the underlying benchmark (SciFact, ContractNLI,
WDC Products, SWE-bench Verified). Skim the field name; if it does
not change your reading, ignore it. The `policy_text`, `prompt`,
`gold_*`, and `verifier_rule` blocks are the only ones the rubric
depends on.

**Q. The hardened task is solvable but takes me 10 minutes of
reading. Is that "natural"?**

Yes — long hardened tasks (especially SWE-bench and SciFact) are
expected. "Natural" means *legitimate as an operator call*, not
*easy*. A task that takes 10 minutes for an expert can still be a 5.

**Q. The gold answer looks wrong to me.**

This is exactly the case the audit cares about. If the gold answer
disagrees with what you, as a domain expert, would call correct,
mark Q2 as `disagree_too_strict` (the verifier insists on a wrong
answer) and explain in `notes`. The paper's retained-disagreement
appendix is built on these.

**Q. I don't know the domain at all.**

Mark `confidence: "low"`. Do not skip. The aggregator can produce a
high-confidence-only headline if needed, but only if every task has
*some* response.

**Q. How do I cite my answers later?**

Each task in the manifest has a stable `task_key`. Notes referenced
by `task_key` survive across re-runs of `build_tasks.py`.
