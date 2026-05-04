# Audit task — contractnli / map

**task_key:** `contract:384/hypothesis:nda-4`  
**task_family:** `hard_map`  
**file stem:** `19_map_contract_384_hypothesis_nda-4`

> Read this page top-to-bottom, then write your two ratings into `responses/<your_name>.json` under the key shown above. See `PROTOCOL.md` for the rubric.

---

## Key facts

*(The inputs the model would see, plus the gold answer with span / sentence ids resolved to their text. These are the facts you actually need to rate Q1 and Q2.)*

**Hypothesis** (the claim about the contract):

> Receiving Party shall not use any Confidential Information for any purpose other than the purposes stated in Agreement.

**Gold label:** `entailment`

**Gold-evidence variants** (each variant is one accepted set of `span_ids`; the verifier accepts any single variant exactly):

- Variant 1: `span_ids = [10, 12]`
  > 3. The Receiving Party expressly agrees not to use the Confidential Information for purposes other than those necessary to consider whether to enter into a Transaction and shall strictly limit its disclosure to such of its employees, directors and advisors having a need to know such information, which parties shall be advised that such information is Confidential Information and subject to the terms of this Agreement.
  > Notwithstanding the termination of this Agreement for any reason, the Receiving Party shall not use the Confidential Information for purposes of competing with the Disclosing Party.


---

## Verifier rule (what the strict verifier checks)

> Output is the structured map record (label + basis + span_ids). Accept iff label matches gold, span_ids form an accepted variant, and the basis enum is consistent with span content (e.g. `direct_support` vs `exception_clause`).

This rule is the contract you are auditing in **Q2**.

---

## Policy / instructions (as the model sees them)

> Return the final NLI label and the exact span ids that justify it from the shown clause inventory. The inventory is intentionally noisy and may include exception-like confusers. Use entailment or contradiction only when the returned spans themselves determine the label. If the hypothesis is not mentioned, return not_mentioned and an empty span_ids list.

---

## Other fields (collapsed, for reference)

<details><summary><code>contract_id</code></summary>

```
384
```

</details>

<details><summary><code>contract_text</code> (truncated)</summary>

```
[SPAN 9] Confidential Information shall also not include information that the parties agree in writing may be disclosed by Receiving Party.
[SPAN 10] 3. The Receiving Party expressly agrees not to use the Confidential Information for purposes other than those necessary to consider whether to enter into a Transaction and shall strictly limit its disclosure to such of its employees, directors and advisors having a need to know such information, which parties shall be advised that such information is Confidential Information and subject to the terms of this Agreement. 
[SPAN 11] Except as set forth herein, the Receiving Party shall hold all information received in confidence and not sell, assign, transfer, release or otherwise disclose the Confidential Information, or material derived therefrom, to any third party, or to its other employees, officers, directors, shareholders, agents or consultants. 
[SPAN 12] Notwithstanding the termination of this Agreement for any reason, the Receiving Party shall not use the Confidential Information for purposes of competing with the Disclosing Party.
[SPAN 13] 4. Except as must be disclosed pursuant to applicable legal disclosure requirements or legal process, neither party nor any of its respective representatives may, without the prior written consent of the other party, disclose to any person (other than to its employees, directors and advisors having a need to know such information) that the parties have exchanged confidential informatio
... [truncated, full content in the .json file] ...
```

</details>

<details><summary><code>inventory_span_ids</code></summary>

```
[
  9,
  10,
  11,
  12,
  13,
  15,
  16,
  17,
  18,
  22
]
```

</details>


---

## Audit questions

**Q1 — Naturalness (1–5).** Does this hardened task still look like a natural operator problem? See `PROTOCOL.md`.

**Q2 — Verifier validity.** Would the verifier rule above accept the same outputs you would accept on this task? Choose `agree`, `disagree_too_strict`, `disagree_too_lax`, or `disagree_other`.

Append your answer to your responses file under the key `"contract:384/hypothesis:nda-4"`. See `responses/EXAMPLE_filled.json`.
