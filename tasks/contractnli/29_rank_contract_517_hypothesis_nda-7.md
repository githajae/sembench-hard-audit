# Audit task — contractnli / rank

**task_key:** `contract:517/hypothesis:nda-7`  
**task_family:** `hard_rank`  
**file stem:** `29_rank_contract_517_hypothesis_nda-7`

> Read this page top-to-bottom, then write your two ratings into `responses/<your_name>.json` under the key shown above. See `PROTOCOL.md` for the rubric.

---

## Key facts

*(The inputs the model would see, plus the gold answer with span / sentence ids resolved to their text. These are the facts you actually need to rate Q1 and Q2.)*

**Hypothesis** (the claim about the contract):

> Receiving Party may share some Confidential Information with some third-parties (including consultants, agents and professional advisors).

**`top_k` (rank length the verifier checks):** `3`

**Gold-positive `span_ids`** (must appear in top-3):
- `span_id = 32` — (b) Confidential Information shall be disclosed only to employees, agents, and other parties of the Receiving Party who have a “need to know” in connection with the purposes stated herein; and


---

## Verifier rule (what the strict verifier checks)

> Output is a ranked list of `span_ids` of length `top_k`. Accept iff each id is a valid contract-span id and the top-`k` set contains every gold-positive span for the hypothesis.

This rule is the contract you are auditing in **Q2**.

---

## Policy / instructions (as the model sees them)

> Rank clause spans by how directly they determine the final contract label for the hypothesis. Gold evidence clauses must appear before confusable but non-evidence clauses.

---

## Other fields (collapsed, for reference)

<details><summary><code>contract_id</code></summary>

```
517
```

</details>


---

## Audit questions

**Q1 — Naturalness (1–5).** Does this hardened task still look like a natural operator problem? See `PROTOCOL.md`.

**Q2 — Verifier validity.** Would the verifier rule above accept the same outputs you would accept on this task? Choose `agree`, `disagree_too_strict`, `disagree_too_lax`, or `disagree_other`.

Append your answer to your responses file under the key `"contract:517/hypothesis:nda-7"`. See `responses/EXAMPLE_filled.json`.
