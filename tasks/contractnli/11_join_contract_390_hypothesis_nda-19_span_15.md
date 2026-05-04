# Audit task — contractnli / join

**task_key:** `contract:390/hypothesis:nda-19/span:15`  
**task_family:** `hard_join`  
**file stem:** `11_join_contract_390_hypothesis_nda-19_span_15`

> Read this page top-to-bottom, then write your two ratings into `responses/<your_name>.json` under the key shown above. See `PROTOCOL.md` for the rubric.

---

## Key facts

*(The inputs the model would see, plus the gold answer with span / sentence ids resolved to their text. These are the facts you actually need to rate Q1 and Q2.)*

**Hypothesis** (the claim about the contract):

> Some obligations of Agreement may survive termination of Agreement.

**Candidate clause** (`span_id = 15`):

> The obligations of this Agreement, including the restrictions on disclosure and use, shall not apply with respect to any Confidential Information to the extent such Confidential Information is

**Gold label:** `not_evidence`

**Confuser / candidate clauses (first 5 shown in full):**

- `span_id = 8` — "CONFIDENTIAL INFORMATION" means any and all information and material disclosed by SABI to Victorinox (before or after the signing of this Agreement, and whether orally or in writing, graphic, electronic or any other form) that is marked or described as, identified orally or in writing as, or provided under circumstances indicating it is, confidential, proprietary or not otherwise available to the general public at the time of such disclosure.
- `span_id = 11` — Victorinox shall disclose the Confidential Information only to its employees and agents who need to know such information and who are bound by restrictions regarding disclosure and use of such information comparable to and no less restrictive than those set forth herein.
- `span_id = 27` — In the event that any of the provisions of this Agreement shall be held by a court or other tribunal of competent jurisdiction to be invalid or unenforceable, the remaining portions hereof shall remain in full force and effect and such provision shall be enforced to the maximum extent possible so as to effect the intent of the parties and shall be reformed to the extent necessary to make such provision valid and enforceable.
- `span_id = 25` — The waiver by either party of a breach of or a default under any provision of this Agreement shall not be construed as a waiver of any subsequent breach of or default under the same or any other provision of this Agreement, nor shall any delay or omission on the part of either party to exercise or avail itself of any right or remedy that it has or may have hereunder operate as a waiver of any right or remedy.
- `span_id = 16` — or becomes publicly known through no act or omission of the Victorinox, or to the extent that disclosure of such Confidential Information is required by law.


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
390
```

</details>

<details><summary><code>span_text</code></summary>

```
The obligations of this Agreement, including the restrictions on disclosure and use, shall not apply with respect to any Confidential Information to the extent such Confidential Information is
```

</details>


---

## Audit questions

**Q1 — Naturalness (1–5).** Does this hardened task still look like a natural operator problem? See `PROTOCOL.md`.

**Q2 — Verifier validity.** Would the verifier rule above accept the same outputs you would accept on this task? Choose `agree`, `disagree_too_strict`, `disagree_too_lax`, or `disagree_other`.

Append your answer to your responses file under the key `"contract:390/hypothesis:nda-19/span:15"`. See `responses/EXAMPLE_filled.json`.
