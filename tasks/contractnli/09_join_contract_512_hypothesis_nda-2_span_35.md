# Audit task — contractnli / join

**task_key:** `contract:512/hypothesis:nda-2/span:35`  
**task_family:** `hard_join`  
**file stem:** `09_join_contract_512_hypothesis_nda-2_span_35`

> Read this page top-to-bottom, then write your two ratings into `responses/<your_name>.json` under the key shown above. See `PROTOCOL.md` for the rubric.

---

## Key facts

*(The inputs the model would see, plus the gold answer with span / sentence ids resolved to their text. These are the facts you actually need to rate Q1 and Q2.)*

**Hypothesis** (the claim about the contract):

> Confidential Information shall only include technical information.

**Candidate clause** (`span_id = 35`):

> Contractor agrees to regard and preserve as confidential all information obtained by Contractor relating or pertaining to

**Gold label:** `evidence`

**Confuser / candidate clauses (first 5 shown in full):**

- `span_id = 46` — Contractor agrees that, upon termination of our contract with the Company (voluntary or otherwise), Contractor will return to the Company all things belonging to the Company, and that all documents, records, notebooks and tangible articles containing or embodying confidential information, including copies thereof, then in our possession or control, whether prepared by Contractor or others, will be left with the Company.
- `span_id = 39` — Contractor further agrees to preserve as confidential the confidential information of any third party to which Contractor may have access and to treat such information as though it were Company confidential information.
- `span_id = 74` — Also, Contractor hereby assigns, and agree to assign, to the Company all Inventions conceived or reduced to practice by Contractor within one year following the termination of our work for the Company (voluntary or otherwise), if the Invention is a result of the Company’s information which was obtained by Contractor during our work for the Company.
- `span_id = 41` — Contractor agrees to promptly advise the Company of any knowledge which Contractor may have of any unauthorized release or use of any Company confidential information, and shall take reasonable measures to prevent unauthorized persons or entities from having access to, obtaining or being furnished with any Company confidential information.
- `span_id = 43` — Contractor agrees not to disclose to the Company and not to use in any way in connection with our work for the Company any confidential information or trade secrets of any kind, or any embodiments thereof, of any previous employer or other third party.


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
512
```

</details>

<details><summary><code>span_text</code></summary>

```
Contractor agrees to regard and preserve as confidential all information obtained by Contractor relating or pertaining to 
```

</details>


---

## Audit questions

**Q1 — Naturalness (1–5).** Does this hardened task still look like a natural operator problem? See `PROTOCOL.md`.

**Q2 — Verifier validity.** Would the verifier rule above accept the same outputs you would accept on this task? Choose `agree`, `disagree_too_strict`, `disagree_too_lax`, or `disagree_other`.

Append your answer to your responses file under the key `"contract:512/hypothesis:nda-2/span:35"`. See `responses/EXAMPLE_filled.json`.
