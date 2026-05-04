# Audit task — contractnli / rank

**task_key:** `contract:111/hypothesis:nda-3`  
**task_family:** `hard_rank`  
**file stem:** `28_rank_contract_111_hypothesis_nda-3`

> Read this page top-to-bottom, then write your two ratings into `responses/<your_name>.json` under the key shown above. See `PROTOCOL.md` for the rubric.

---

## Key facts

*(The inputs the model would see, plus the gold answer with span / sentence ids resolved to their text. These are the facts you actually need to rate Q1 and Q2.)*

**Hypothesis** (the claim about the contract):

> Confidential Information may include verbally conveyed information.

**`top_k` (rank length the verifier checks):** `3`

**Gold-positive `span_ids`** (must appear in top-3):
- `span_id = 17` — For the purposes of this Agreement, the term “Confidential Information” shall include, but not be limited to, documents, records, information and data (whether verbal, electronic or written), drawings, models, apparatus, sketches, designs, schedules, product plans, marketing plans, technical procedures, manufacturing processes, analyses, compilations, studies, software, prototypes, samples, formulas, methodologies, formulations, product developments, patent applications, know-how, experimental results, specifications and other business information, relating to the Party’s business, assets, operations or contracts, furnished to the other Party and/or the other Party’s affiliates, employees, officers, owners, agents, consultants or representatives, in the course of their work contemplated in this Agreement, regardless of whether such Confidential Information has been expressly designated as confidential or proprietary.
- `span_id = 18` — Confidential Information also includes any and all, work products, studies and other material prepared by or in the possession or control of the other Party, which contain, include, refer to or otherwise reflect or are generated from any Confidential Information.


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
111
```

</details>


---

## Audit questions

**Q1 — Naturalness (1–5).** Does this hardened task still look like a natural operator problem? See `PROTOCOL.md`.

**Q2 — Verifier validity.** Would the verifier rule above accept the same outputs you would accept on this task? Choose `agree`, `disagree_too_strict`, `disagree_too_lax`, or `disagree_other`.

Append your answer to your responses file under the key `"contract:111/hypothesis:nda-3"`. See `responses/EXAMPLE_filled.json`.
