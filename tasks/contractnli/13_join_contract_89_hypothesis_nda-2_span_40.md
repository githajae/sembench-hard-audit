# Audit task — contractnli / join

**task_key:** `contract:89/hypothesis:nda-2/span:40`  
**task_family:** `hard_join`  
**file stem:** `13_join_contract_89_hypothesis_nda-2_span_40`

> Read this page top-to-bottom, then write your two ratings into `responses/<your_name>.json` under the key shown above. See `PROTOCOL.md` for the rubric.

---

## Key facts

*(The inputs the model would see, plus the gold answer with span / sentence ids resolved to their text. These are the facts you actually need to rate Q1 and Q2.)*

**Hypothesis** (the claim about the contract):

> Confidential Information shall only include technical information.

**Candidate clause** (`span_id = 40`):

> B. The headings and other captions in this Agreement are for convenience and reference only and shall not be used in interpreting, construing or enforcing any of the provisions of this agreement.

**Gold label:** `not_evidence`

**Confuser / candidate clauses (first 5 shown in full):**

- `span_id = 51` — Recipient shall not make, have made, use or sell for any purpose any product or other item using, incorporating or derived from Data, other than for the purpose stated in Attachment B for which the Data was provided under this Agreement.
- `span_id = 61` — The Data provided under this Agreement shall be used and maintained in accordance with applicable provisions of federal, state, and local laws, rules and regulations as are in effect at the time the Data is produced by DOHMH and retained by Data Recipient.
- `span_id = 63` — 1. Only the Data Recipient’s employees and/or consultants required to use the Data to perform the functions of this Agreement that are set forth in Attachment B, and so designated by Data Recipient as “Authorized Users” in Attachment C to this Agreement, will be given access to the Data.
- `span_id = 156` — Attachment B to this Agreement, which describes the uses that the Data Recipient may make of the Data, the Data Recipient may publish or publicly present its work as described in Attachment B, which must not contain any individually identifiable information, of the use undertaken in accord with Attachment B. Prior to publication or public presentation of such work product, the Data Recipient will submit its final work product to the DOHMH for review and approval.
- `span_id = 189` — If any provision of this Agreement is found by a proper authority to be unenforceable or invalid, such unenforceability or invalidity shall not render this Agreement unenforceable or invalid as a whole and, in such event, such provision shall be changed and interpreted so as to best accomplish the objectives of such unenforceable or invalid provision within the limits of applicable law or applicable court decisions.


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
89
```

</details>

<details><summary><code>span_text</code></summary>

```
B. The headings and other captions in this Agreement are for convenience and reference only and shall not be used in interpreting, construing or enforcing any of the provisions of this agreement.
```

</details>


---

## Audit questions

**Q1 — Naturalness (1–5).** Does this hardened task still look like a natural operator problem? See `PROTOCOL.md`.

**Q2 — Verifier validity.** Would the verifier rule above accept the same outputs you would accept on this task? Choose `agree`, `disagree_too_strict`, `disagree_too_lax`, or `disagree_other`.

Append your answer to your responses file under the key `"contract:89/hypothesis:nda-2/span:40"`. See `responses/EXAMPLE_filled.json`.
