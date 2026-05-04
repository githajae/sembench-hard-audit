# Audit task — contractnli / rank

**task_key:** `contract:385/hypothesis:nda-10`  
**task_family:** `hard_rank`  
**file stem:** `30_rank_contract_385_hypothesis_nda-10`

> Read this page top-to-bottom, then write your two ratings into `responses/<your_name>.json` under the key shown above. See `PROTOCOL.md` for the rubric.

---

## Key facts

*(The inputs the model would see, plus the gold answer with span / sentence ids resolved to their text. These are the facts you actually need to rate Q1 and Q2.)*

**Hypothesis** (the claim about the contract):

> Receiving Party shall not disclose the fact that Agreement was agreed or negotiated.

**`top_k` (rank length the verifier checks):** `3`

**Gold-positive `span_ids`** (must appear in top-3):
- `span_id = 40` — Neither party hereto shall publicly announce or otherwise disclose, without the prior written consent of the other, any proposed terms of or that discussions relating to the Transaction are taking place except for such disclosure as the party seeking to make disclosure has been advised by its legal counsel is required by law, in which case the party seeking to make disclosure shall provide the other party with as much prior notice of such announcement or disclosure (including the proposed text of such announcement or disclosure) as is reasonably possible under the circumstances (and attempt in good faith to obtain such other party's concurrence with the manner and extent of such disclosure).


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
385
```

</details>


---

## Audit questions

**Q1 — Naturalness (1–5).** Does this hardened task still look like a natural operator problem? See `PROTOCOL.md`.

**Q2 — Verifier validity.** Would the verifier rule above accept the same outputs you would accept on this task? Choose `agree`, `disagree_too_strict`, `disagree_too_lax`, or `disagree_other`.

Append your answer to your responses file under the key `"contract:385/hypothesis:nda-10"`. See `responses/EXAMPLE_filled.json`.
