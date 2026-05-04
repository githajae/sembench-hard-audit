# Audit task — contractnli / map

**task_key:** `contract:89/hypothesis:nda-18`  
**task_family:** `hard_map`  
**file stem:** `21_map_contract_89_hypothesis_nda-18`

> Read this page top-to-bottom, then write your two ratings into `responses/<your_name>.json` under the key shown above. See `PROTOCOL.md` for the rubric.

---

## Key facts

*(The inputs the model would see, plus the gold answer with span / sentence ids resolved to their text. These are the facts you actually need to rate Q1 and Q2.)*

**Hypothesis** (the claim about the contract):

> Receiving Party shall not solicit some of Disclosing Party's representatives.

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
89
```

</details>

<details><summary><code>contract_text</code> (truncated)</summary>

```
[SPAN 53] Upon written request by DOHMH, Data Recipient shall promptly return to DOHMH Data, notes, and other tangible materials representing the Data and all copies and reproduction thereof (in whole or in part) and shall delete or otherwise destroy any copies or reproductions of such Data that may reside in Data Recipient’s possession, including but not limited to, on Data Recipient’s server, computer systems, or files.
[SPAN 107] Except as set forth in Section III, Data Recipient shall not reproduce the Data in any form without the prior written consent of DOHMH.
[SPAN 118] A. Any waiver by DOHMH of any act, failure to act or breach on the part of Data Recipient shall not constitute a waiver by DOHMH of any prior or subsequent act or failure to act or breach by Data Recipient and shall not be effective unless set forth in a written document executed by DOHMH.
[SPAN 132] Either Party may change its contact information by notice to the other; any such change shall take effect immediately upon delivery of such notice. 
[SPAN 152] A. Data Recipient shall not reveal any individual identifying information such as a person’s date of birth, last name, first name, or any other identifying information in any draft or final publication.
[SPAN 172] A. The Data Recipient agrees that it shall not subcontract, assign, transfer, convey or otherwise dispose of its obligations under this Agreement except by operation of law, without the prior written consent of the other party.
[SPAN 180] F
... [truncated, full content in the .json file] ...
```

</details>

<details><summary><code>inventory_span_ids</code></summary>

```
[
  53,
  107,
  118,
  132,
  152,
  172,
  180,
  182,
  183,
  189
]
```

</details>


---

## Audit questions

**Q1 — Naturalness (1–5).** Does this hardened task still look like a natural operator problem? See `PROTOCOL.md`.

**Q2 — Verifier validity.** Would the verifier rule above accept the same outputs you would accept on this task? Choose `agree`, `disagree_too_strict`, `disagree_too_lax`, or `disagree_other`.

Append your answer to your responses file under the key `"contract:89/hypothesis:nda-18"`. See `responses/EXAMPLE_filled.json`.
