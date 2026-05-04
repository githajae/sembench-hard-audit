# Audit task — contractnli / rank

**task_key:** `contract:231/hypothesis:nda-3`  
**task_family:** `hard_rank`  
**file stem:** `24_rank_contract_231_hypothesis_nda-3`

> Read this page top-to-bottom, then write your two ratings into `responses/<your_name>.json` under the key shown above. See `PROTOCOL.md` for the rubric.

---

## Key facts

*(The inputs the model would see, plus the gold answer with span / sentence ids resolved to their text. These are the facts you actually need to rate Q1 and Q2.)*

**Hypothesis** (the claim about the contract):

> Confidential Information may include verbally conveyed information.

**`top_k` (rank length the verifier checks):** `3`

**Gold-positive `span_ids`** (must appear in top-3):
- `span_id = 10` — 1.4. The Proprietary Information is any information of the Company marked as «Commercial Secret» or «Conﬁdential» with actual or potential commercial value by virtue of the fact third-parties are unfamiliar with it, submitted to the Investor by the Company in written form by documents transmission, including the electronic transmission of documents secured from unauthorized access to the transmitted information, the information related to business or ﬁnance plans and strategies including, without limitation information about markets, ﬁnancial documents, ﬁnancial statements and accounting (except for cases deﬁned by law), contractual relationships, pricing and marketing of goods (works and services), technical information, commercial secrets, know-how, research, production schedules, concepts, intellectual activity property (which includes discoveries, inventions, rationalization proposals, utility models, constructions, industrial models that are non-proprietary for some reasons, computer software, databases, logotypes scratches that are non-registered for some reasons).


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
231
```

</details>


---

## Audit questions

**Q1 — Naturalness (1–5).** Does this hardened task still look like a natural operator problem? See `PROTOCOL.md`.

**Q2 — Verifier validity.** Would the verifier rule above accept the same outputs you would accept on this task? Choose `agree`, `disagree_too_strict`, `disagree_too_lax`, or `disagree_other`.

Append your answer to your responses file under the key `"contract:231/hypothesis:nda-3"`. See `responses/EXAMPLE_filled.json`.
