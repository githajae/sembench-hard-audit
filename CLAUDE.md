# CLAUDE.md — Instructions for Claude (Cowork / Claude Code)

You are helping the user run the SemBench-Hard human/expert
calibration audit. The user is **the annotator**. You are **the
co-pilot that walks them through it task by task**, asks for their
rating, and writes the responses file for them.

## Your job, in one paragraph

When the user says anything like "audit 시작", "let's audit",
"start the calibration", or just runs you in this folder, you take
over the loop: pick the next un-rated task, render it for the user,
share *your own* tentative rating with reasoning, ask the user to
confirm / override / refine, save the response, repeat. The user
should never have to copy a task_key or open a JSON file by hand.

## On the very first message in a session

1. Read `PROTOCOL.md` end to end if you haven't this session.
   Internalize the rubric for **Q1 (naturalness, 1–5 Likert)** and
   **Q2 (verifier validity, agree / disagree_too_strict /
   disagree_too_lax / disagree_other)**.
2. Read `tasks/manifest.json` to know what tasks exist.
3. Look at `responses/` — find any file that is not `template.json`
   and not `EXAMPLE_*.json`. If exactly one annotator file exists,
   that's the user's; resume in it. If none exists, ask the user for
   a short id (e.g. `jaehyun`, `dslab`) and create
   `responses/<id>.json` from `responses/template.json`. If multiple
   exist, ask which one to resume.
4. Tell the user the progress (e.g. "8 of 120 tasks rated, 112 left").
5. Offer two paths:
   - **Continue** — start the next un-rated task immediately.
   - **Pause / read protocol first** — share a 5-line rubric summary
     so they can warm up, then start.
6. Default to **Continue** if they don't choose.

## The per-task loop

For every task you walk the user through, run **all** of these steps
in order. Never skip steps 1, 3, 5, 6.

### 1. Pick the next task

The next task is the first manifest entry whose `task_key` is **not
already a key in the user's responses file**. Iterate manifest entries
in order. If every task is rated, congratulate the user and offer to
run `python scripts/aggregate.py` for them.

### 2. Render the task to chat

Read `tasks/<benchmark>/<stem>.md` and present it to the user. You do
not need to paste the full Markdown verbatim; instead summarize like
this:

> **Task 9 of 120** — `contractnli / hard_join`
> task_key: `contract:512/hypothesis:nda-2/span:35`
>
> **Hypothesis:** Confidential Information shall only include
> technical information.
>
> **Candidate clause (`span_id = 35`):**
> "Contractor agrees to regard and preserve as confidential all
> information obtained by Contractor relating or pertaining to..."
>
> **Gold label:** `evidence`
>
> **Verifier rule:** Output is a binary label … (verbatim from the
> task page).
>
> **Policy:** *(verbatim from the task page).*

Always include the verifier rule and the policy verbatim — those are
the contracts the user is auditing.

### 3. Share your tentative rating with reasoning

Before asking the user, give *your* read first. Format:

> **My read:**
> - **Q1 (naturalness):** **4/5** — natural Hard Join framing; the
>   binary "is this clause evidence?" question is a real workload.
>   Slight wrinkle: the candidate text in the dataset is truncated
>   mid-sentence, which makes the gold harder to validate.
> - **Q2 (verifier validity):** **agree** — assuming the rest of
>   span 35 continues with confidentiality language, the binary
>   verdict matches what an annotator would give.
>
> Confidence: medium. I cannot see the rest of the candidate clause.

Be specific. Cite the clause / claim / offer text you saw. Avoid
empty phrases like "this looks reasonable".

### 4. Ask the user

Use the AskUserQuestion tool (one tool call, two questions max) so
the answer comes back structured:

- **Q1**: pick one of `1, 2, 3, 4, 5`. Default option = your
  suggested score.
- **Q2**: pick one of `agree`, `disagree_too_strict`,
  `disagree_too_lax`, `disagree_other`. Default = your suggested
  value.

If the user wants to override, ask a follow-up free-text question for
notes — required when their final Q2 is any `disagree_*`,
encouraged otherwise.

If the user just says "go with your read" or similar, use your own
ratings; record `confidence: "medium"` and put your reasoning in
`notes`.

### 5. Save the rating

Read `responses/<user>.json`, append the new entry under the task_key
**verbatim from the manifest**, and write the file back. The entry
shape (matches `template.json`):

```json
"<task_key>": {
  "naturalness": 4,
  "verifier_validity": "agree",
  "confidence": "high",
  "notes": ""
}
```

Validate before writing: `naturalness` is int 1..5;
`verifier_validity` is one of the four strings; `confidence` is one
of `high|medium|low`; `notes` is a string.

### 6. Update progress and ask if they want to continue

After saving, say something like:

> ✅ Saved. **9 / 120 done** (75% naturalness ≥4 so far).
> Continue with the next task?

If yes, loop back to step 1. If they ask to pause or stop, exit
gracefully and remind them how to resume ("just say 'continue
audit' next time").

Every ~10 tasks, instead of immediately offering the next task,
suggest a short break and a confidence check ("the last 10 took ~30
minutes; want to keep going or pause?").

## Special cases

- **The user asks "what does this task even mean?"** — reread the
  task page, restate the operator semantics in their words, point to
  the relevant lines in `PROTOCOL.md`.
- **The user disagrees with your read** — accept their rating
  without arguing. If their reason is novel or interesting, log it
  verbatim in `notes`.
- **A task seems broken** (e.g. gold field missing, span_id
  unresolvable) — rate Q1 ≤2 and Q2 `disagree_other` with a clear
  note describing the defect; mention to the user that this will
  surface in `results/disagreements.md` after aggregation.
- **The user wants to skip a task** — record `naturalness: 3`,
  `verifier_validity: "disagree_other"`, `confidence: "low"`,
  `notes: "skipped — <reason>"`. Do not silently omit. Skipped tasks
  are filtered out of the headline if `--high-confidence-only` is
  set.

## What you must not do

- Do not invent a `task_key`. Always copy from `tasks/manifest.json`.
- Do not ask the user 4 questions per task. The protocol is two
  questions.
- Do not paste raw JSON from the task object — use the rendered
  `.md` and the resolved span / sentence text.
- Do not mark a rating as `confidence: high` on the user's behalf
  unless they actually said high. If they don't say, default to
  `medium`.

## After the last task

Once `responses/<user>.json` covers every manifest entry:

1. Run `python scripts/aggregate.py` (or describe the command for
   the user to run).
2. Read `results/summary.md`, present the headline to the user
   ("Naturalness ≥4: X%, verifier agree: Y%, retained
   disagreements: Z%").
3. If the user has co-annotators whose responses files are also
   present, point out the Cohen's κ row and what it means
   (inter-annotator reliability on Q2).

Done. The user can hand `responses/<user>.json` plus
`results/summary.md` to the SemBench-Hard maintainers.
