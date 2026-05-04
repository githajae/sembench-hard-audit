# Audit task — contractnli / map

**task_key:** `contract:119/hypothesis:nda-15`  
**task_family:** `hard_map`  
**file stem:** `22_map_contract_119_hypothesis_nda-15`

> Read this page top-to-bottom, then write your two ratings into `responses/<your_name>.json` under the key shown above. See `PROTOCOL.md` for the rubric.

---

## Key facts

*(The inputs the model would see, plus the gold answer with span / sentence ids resolved to their text. These are the facts you actually need to rate Q1 and Q2.)*

**Hypothesis** (the claim about the contract):

> Agreement shall not grant Receiving Party any right to Confidential Information.

**Gold label:** `not_mentioned`

**Gold-evidence variants** (each variant is one accepted set of `span_ids`; the verifier accepts any single variant exactly):

- Variant 1: `span_ids = []`
  > *(empty: only valid for `not_mentioned`)*


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
119
```

</details>

<details><summary><code>contract_text</code> (truncated)</summary>

```
[SPAN 3] THIS UNDERTAKING IS TO BE MADE BY ALL PERSONS, NATURAL AND LEGAL, (THE VENDOR) WHO ARE GIVEN ACCESS, FOR WHATEVER PURPOSE, TO ANY INFORMATION, CONSIDERED BY GRINDROD SA, TO BE CONFIDENTIAL (AS DEFINED IN THIS UNDERTAKING). 
[SPAN 7] 1.1 “Confidential Information” means; all technical, commercial, procurement requirements, purchasing, manufacturing, customer lists, investors, employees, business and contractual relationships, business forecasts, sales and merchandising, and marketing plans business or personnel information disclosed or otherwise made available in any format and/or physical manner by Grindrod SA or becoming available, before, during and/or after the execution of an interaction, duty or obligation including all information that makes itself known to the Vendor or comes into being as a result of the rendering, production and/or delivery of an agreement/understanding/request for quotation/contract or Purchase Order, or any other interaction. 
[SPAN 8] Confidential Information shall also include any other information that is marked as "Confidential" or should reasonably be considered confidential Confidential Information excludes information which is already in the possession, or under the control of the Vendor otherwise than as a result of having been disclosed by Grindrod SA to the Vendor or as a result of the preparation and execution of a proposal or any other interaction with Grindrod SA. 
[SPAN 9] Confidential Information also excludes information in
... [truncated, full content in the .json file] ...
```

</details>

<details><summary><code>inventory_span_ids</code></summary>

```
[
  3,
  7,
  8,
  9,
  15,
  16,
  19,
  21,
  23,
  27
]
```

</details>


---

## Audit questions

**Q1 — Naturalness (1–5).** Does this hardened task still look like a natural operator problem? See `PROTOCOL.md`.

**Q2 — Verifier validity.** Would the verifier rule above accept the same outputs you would accept on this task? Choose `agree`, `disagree_too_strict`, `disagree_too_lax`, or `disagree_other`.

Append your answer to your responses file under the key `"contract:119/hypothesis:nda-15"`. See `responses/EXAMPLE_filled.json`.
