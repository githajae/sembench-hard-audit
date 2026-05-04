# LLM Co-Pilot Prompt

> Use this only as a co-pilot — your final ratings must be your own.
> The protocol described in `PROTOCOL.md` assumes informed human
> judgment.

Copy everything between the two `BEGIN PROMPT` / `END PROMPT` markers
into a chat model (Claude, GPT-4, Gemini, …), then paste **one task's
`.json` file** at the end where the prompt asks.

---

## How to use

1. Pick a task, e.g. `tasks/scifact/03_join_claim_42_doc_4983040.json`.
2. Open the file in a text editor; copy its contents.
3. Open a fresh chat with your LLM.
4. Paste the prompt below, then paste the task JSON immediately after
   `<<<TASK_JSON>>>`.
5. Read the model's response. Use its rationale to challenge or
   confirm your reading. Do **not** copy its answer verbatim.

---

```
==================== BEGIN PROMPT ====================

You are helping audit a hardened benchmark of declarative semantic
operators (Map, Filter, Join, Rank). For each task, the dataset
provides a policy, a prompt, a gold/accepted answer, and a strict
verifier rule. The audit asks two calibration questions:

(Q1) Task naturalness — would an experienced data engineer find this
     a natural operator call to make? Score on a 5-point Likert:
     5 = completely natural,
     4 = mostly natural with a minor wrinkle,
     3 = borderline / recognisable but rigid,
     2 = awkward, multiple reasonable interpretations,
     1 = unnatural / broken.

(Q2) Verifier validity — would the strict verifier accept the same
     outputs that a competent domain-aware annotator would accept?
     Answer one of:
       agree                  — verifier and annotator align,
       disagree_too_strict    — verifier rejects outputs annotator accepts,
       disagree_too_lax       — verifier accepts outputs annotator rejects,
       disagree_other         — describe.

Process each task in three steps:

  Step 1. Restate the operator call in one sentence. What is the
          system being asked to do, in plain language?

  Step 2. Rate Q1. Cite the specific feature of the task (the policy
          text, the schema, the constraint, the verification axis)
          that drove your score up or down. Be concrete.

  Step 3. Rate Q2. Construct one plausible correct answer and one
          plausible wrong-but-close answer. Walk the verifier rule
          over both and decide whether the verifier's accept/reject
          matches what an informed annotator would conclude.

Output format (must be valid JSON, on the last line of your response):

  {"q1_score": <1..5>, "q1_reason": "<≤200 chars>",
   "q2_value": "<agree|disagree_too_strict|disagree_too_lax|disagree_other>",
   "q2_reason": "<≤300 chars>"}

You may write reasoning before that JSON. Do not include any text
after the JSON.

The task object follows. All fields are dataset-defined; ignore
fields that do not affect the operator semantics.

<<<TASK_JSON>>>

==================== END PROMPT ====================
```

---

## Notes for using the output

- Compare the LLM's `q1_score` with your own. If you disagree by ≥2
  points, re-read the task page — usually one of you missed a
  policy clause.
- Compare the `q2_value`. LLMs tend to default to `agree` because
  they are trained to be charitable. Treat any `disagree_*` answer
  from the LLM as a strong signal worth investigating.
- Do **not** paste the LLM JSON into your responses file as-is. Use
  it to challenge your own thinking, then write your own values.

## Sanity-check the LLM's reasoning

A good co-pilot answer:

- restates the operator call **in your own domain's vocabulary**,
- points to a specific clause in the policy/schema/verifier when
  scoring,
- constructs a concrete wrong-but-close answer when reasoning about
  Q2.

A bad co-pilot answer:

- says "this looks reasonable" without grounding,
- misreads the verifier rule (e.g. ignores citation requirements),
- gives a Q1 score and a Q2 value that contradict each other (e.g.
  `q1_score: 1` but `q2_value: agree`).

If the LLM's answer is in the "bad" pattern, ignore it and trust
your own reading.
