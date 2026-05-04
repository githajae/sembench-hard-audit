# Audit task — contractnli / join

**task_key:** `contract:135/hypothesis:nda-19/span:41`  
**task_family:** `hard_join`  
**file stem:** `15_join_contract_135_hypothesis_nda-19_span_41`

> Read this page top-to-bottom, then write your two ratings into `responses/<your_name>.json` under the key shown above. See `PROTOCOL.md` for the rubric.

---

## Key facts

*(The inputs the model would see, plus the gold answer with span / sentence ids resolved to their text. These are the facts you actually need to rate Q1 and Q2.)*

**Hypothesis** (the claim about the contract):

> Some obligations of Agreement may survive termination of Agreement.

**Candidate clause** (`span_id = 41`):

> 8. The terms of this Agreement supersede any previous non-disclosure agreements or any other preliminary representations or understandings that have been entered into by the parties to this Agreement with regard to the subject CONFIDENTIAL INFORMATION.

**Gold label:** `not_evidence`

**Confuser / candidate clauses (first 5 shown in full):**

- `span_id = 26` — shall not be disclosed or revealed to anyone except employees of RECIPIENT who have a need to know the CONFIDENTIAL INFORMATION for the PURPOSE and who agree to be bound by the terms of this Agreement.
- `span_id = 37` — 6. It is understood that nothing herein shall be deemed to constitute, by implication or otherwise, the grant to RECIPIENT of any license or other rights under any patent, patent application, or other intellectual property right or interest belonging to PROVIDER, or as permitting RECIPIENT to unfairly obtain the right to use any CONFIDENTIAL INFORMATION which becomes publicly known through an improper act or omission on its part.
- `span_id = 31` — (b) that can be demonstrated, from written records, to have been in RECIPIENT's possession or readily available to RECIPIENT from another source not under obligation of secrecy to PROVIDER prior to the disclosure; or
- `span_id = 30` — (a) that can be demonstrated to have been in the public domain or publicly known and readily available to the trade or the public prior to the date of the disclosure; or
- `span_id = 28` — However, RECIPIENT agrees that it will not use the CONFIDENTIAL INFORMATION for any purpose other than the PURPOSE without the prior written consent of PROVIDER.


---

## Verifier rule (what the strict verifier checks)

> Output is a binary label for the (candidate clause, hypothesis) pair: `evidence` if the candidate's `span_id` is the supporting evidence for the hypothesis under the gold annotation, else `not_evidence`. Accept iff `label` matches the gold.

This rule is the contract you are auditing in **Q2**.

---

## Policy / instructions (as the model sees them)

> Return evidence only if the candidate clause directly determines the final contract label for the hypothesis. Ignore nearby clauses that merely restate keywords or discuss related exceptions.

---

## Other fields (collapsed, for reference)

<details><summary><code>contract_id</code></summary>

```
135
```

</details>

<details><summary><code>span_text</code></summary>

```
8. The terms of this Agreement supersede any previous non-disclosure agreements or any other preliminary representations or understandings that have been entered into by the parties to this Agreement with regard to the subject CONFIDENTIAL INFORMATION.
```

</details>


---

## Audit questions

**Q1 — Naturalness (1–5).** Does this hardened task still look like a natural operator problem? See `PROTOCOL.md`.

**Q2 — Verifier validity.** Would the verifier rule above accept the same outputs you would accept on this task? Choose `agree`, `disagree_too_strict`, `disagree_too_lax`, or `disagree_other`.

Append your answer to your responses file under the key `"contract:135/hypothesis:nda-19/span:41"`. See `responses/EXAMPLE_filled.json`.
