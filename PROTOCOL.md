# Audit Protocol — The Two Questions

> Read time: ~10 minutes. **Required reading for annotators.**

For every one of the 120 hardened tasks, you answer exactly two
questions and (optionally) leave a note. The aggregator script reads
the structured fields. The note is for the qualitative appendix and
for resolving retained disagreements.

---

## Q1. Task naturalness — 5-point Likert

> *"Does this hardened task still look like a natural operator
> problem? That is, would an experienced data engineer working with
> a declarative `{Map, Filter, Join, Rank}` operator find this a
> reasonable thing to ask the system to do?"*

### Rubric

| Score | Meaning |
| --- | --- |
| **5** | Looks completely natural. The hardened wording is consistent with how a practitioner would phrase the operator call. The added context, constraint, schema, or verification axis only sharpens the request — it does not make the task feel artificial. |
| **4** | Mostly natural with a minor wrinkle. There is a small awkwardness (e.g. the constraint is more pedantic than usual, or the schema is slightly verbose), but a competent reader still recognises the underlying operator problem and would not refuse to attempt it. |
| **3** | Borderline. The task is recognisable, but the hardening introduces enough rigidity that the framing feels test-set-y. A real practitioner might rewrite the call before running it, but the underlying question is still legitimate. |
| **2** | Awkward. The hardening makes the operator call read like a trick question rather than a real workload. Either multiple reasonable interpretations exist, or the strict framing forces an answer that does not match operator semantics. |
| **1** | Unnatural / broken. No competent practitioner would write this operator call this way. The hardening corrupts the underlying task — for example, it requires guessing a hidden convention, or the policy contradicts what the operator name implies. |

The headline metric is **`% of tasks rated ≥ 4`**. The paper reports
87%.

### Examples (illustrative — not from your task set)

- **Score 5.** A SciFact `Filter` task asks: *"Keep claim–paper pairs
  where the abstract directly asserts or denies the claim, with
  sentence-level citations."* Domain-aware reader: yes, that is
  exactly the kind of thing a scientific evidence-extraction
  pipeline does.
- **Score 3.** A ContractNLI `Rank` task asks for the top 3 spans by
  relevance to a hypothesis, but defines "relevance" with an
  unusually long policy statement. Recognisable, but somewhat
  pedantic.
- **Score 1.** A `Map` task hardened so aggressively that the
  required output schema cannot be satisfied without information
  not present in the input.

### What to do if you cannot tell

If the task is in a domain you do not know well — for either Q1 or
Q2 — mark `confidence: "low"` and answer your best guess. **Do not**
skip the task; partial coverage breaks the per-benchmark stats. The
aggregator can optionally exclude `low` confidence ratings from the
headline (`--high-confidence-only`) so honestly-marked low-confidence
answers are not penalised.

---

## Q2. Verifier validity — binary

> *"On this task, would the strict verifier accept the same outputs
> that you, as a domain-aware annotator, would accept?"*

You will see three things on each task page, in the **Key facts**
block:

- The **inputs** the model would see — hypothesis / claim / candidate
  clause / offer pair / issue, as appropriate for the benchmark.
- The **gold answer / accepted variants** with span ids and sentence
  ids **resolved to their actual text**, so you can read the gold
  evidence directly without chasing ids.
- The **verifier rule** — what the strict verifier checks
  (e.g. *"label must be `support`, and `sentence_ids` must equal one
  of the accepted variants exactly"*). This is in its own block right
  below Key facts.

The full task object is preserved in the sibling `.json` file in case
you want to feed it to the LLM co-pilot, but you should be able to
answer Q1 and Q2 from the Key facts block alone.

### Decision rule

You answer one of:

| Value | Meaning |
| --- | --- |
| `agree` | The verifier accepts exactly the outputs a competent annotator would accept on this task. (No false accepts and no false rejects you can spot.) |
| `disagree_too_strict` | The verifier rejects outputs you would accept (e.g., it requires a specific subset of evidence sentences when several reasonable subsets are equivalent). |
| `disagree_too_lax` | The verifier accepts outputs you would reject (e.g., it counts a label-only answer as correct without checking citations). |
| `disagree_other` | A disagreement that is not a simple strict/lax mismatch — describe in the note. |

The headline metric for Q2 is **`% answered "agree"`** (treating any
disagree value as a non-agree). The paper reports 92%.

We additionally compute **Cohen's κ for inter-annotator agreement on
Q2.** The aggregator collapses every annotator's answer to a binary
`agree` vs `disagree` label, then computes κ over every pair of
annotators on the tasks they both rated, and reports the mean across
pairs. The paper reports κ = 0.78. (This is not a verifier-vs-human
κ — it is a reliability check that two informed humans give the same
verifier-validity judgement.)

### Practical heuristics

- The verifier checks whatever is written in the **"Verifier rule"**
  block on the task page. If you find yourself disagreeing because
  the verifier *should* check something it doesn't, that is
  `disagree_too_lax`. If it checks too much, that is
  `disagree_too_strict`.
- If a task has multiple accepted variants and the verifier requires
  one of them, that is **agree** as long as you also think those are
  the reasonable answers.
- If the verifier is stricter than you expected but you ultimately
  think the strictness is justified by the operator semantics
  (e.g. exact citation requirements), choose **agree** with a note.

---

## Confidence and notes

Every answer carries an optional `confidence` and `notes` field:

- `confidence`: `"high"`, `"medium"`, or `"low"`. Mark `"low"` if the
  domain is outside your expertise. The aggregator can optionally
  exclude `"low"` from the headline rates.
- `notes`: free-text. **Strongly encouraged** when you select any
  `disagree_*` value on Q2 — without a note, the retained-disagreement
  appendix in the paper has nothing to cite for that case. The
  aggregator emits a warning (not an error) when a `disagree_*` answer
  is missing notes, so don't rely on it to catch you. **Notes feed
  the retained-disagreement appendix.**

---

## What "retained disagreement" means

After both annotators finish, the aggregator marks a task as a
**retained disagreement** if either:

- The two annotators disagree on Q2 (one says `agree`, the other says
  any `disagree_*`), OR
- Both annotators say `disagree_*` (regardless of subtype).

The paper reports these retained disagreements at 8%, primarily
evidence-ambiguity and gold-variant cases. They are *not* errors in
the audit — they are the qualitative material the paper builds the
"limits of the verifier" discussion on.

---

## Decision flowchart (for a single task)

```
read task page (≤2 min)
   │
   ▼
Q1 — is the hardened task natural? (1–5)
   │
   ▼
Q2 — would the verifier match my judgment? (agree / disagree_*)
   │
   ▼
optional: notes, confidence
   │
   ▼
write entry into responses/<your_name>.json
```

**Time budget.** Pace varies a lot by benchmark:

- WDC Products: ~1.5 min/task (short text, clear pair).
- ContractNLI: ~3 min/task (clauses can be long, exception
  reasoning slows you down).
- SciFact: ~3 min/task (you need to read abstract sentences).
- SWE-bench Verified: 5–10 min/task (real Python diffs and tests
  take time even for experts).

Realistic full-set budget for one annotator: **6–8 hours** of
focused work, ideally split across two sittings (one per benchmark
pair).
