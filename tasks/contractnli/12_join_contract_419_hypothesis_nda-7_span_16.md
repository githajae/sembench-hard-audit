# Audit task — contractnli / join

**task_key:** `contract:419/hypothesis:nda-7/span:16`  
**task_family:** `hard_join`  
**file stem:** `12_join_contract_419_hypothesis_nda-7_span_16`

> Read this page top-to-bottom, then write your two ratings into `responses/<your_name>.json` under the key shown above. See `PROTOCOL.md` for the rubric.

---

## Key facts

*(The inputs the model would see, plus the gold answer with span / sentence ids resolved to their text. These are the facts you actually need to rate Q1 and Q2.)*

**Hypothesis** (the claim about the contract):

> Receiving Party may share some Confidential Information with some third-parties (including consultants, agents and professional advisors).

**Candidate clause** (`span_id = 16`):

> 4. Vendor and Ingram mutually agree that Ingram's public disclosure of the Proprietary Information, except pursuant to a confidential disclosure agreement, to any party will release Vendor from the obligation of confidentiality with respect to that portion of the Proprietary Information actually disclosed by Ingram.

**Gold label:** `not_evidence`

**Confuser / candidate clauses (first 5 shown in full):**

- `span_id = 15` — 3. Vendor and Ingram mutually agree that all copies of the Proprietary Information and all written descriptions, extractions, or summaries thereof, whether made by Vendor or Ingram, shall be the property of Ingram, and shall, upon expiration of this Agreement or Ingram's request, be immediately returned to Ingram.
- `span_id = 17` — 5. Upon termination of this Agreement by either party for any reason, Vendor shall return all Proprietary Information to Ingram within thirty (30) days, irrespective of format.
- `span_id = 20` — In the event that any provision is found invalid or unenforceable pursuant to statutory or Judicial decree, such provision shall be construed only to the maximum extent permitted by law, and the remainder of the Agreement shall be valid and enforceable in accordance with its terms.
- `span_id = 11` — Vendor agrees not to communicate, disclose, or otherwise make available all or any part of the Proprietary Information to any third party, including, but not limited to Vendor's parent, subsidiaries, or affiliated companies.
- `span_id = 13` — Vendor agrees to make no more than five (5) copies of the Proprietary Information unless otherwise agreed in writing between the parties; and Vendor agrees to limit distribution of and access to the Proprietary Information to those of Vendor's personnel who require access to Proprietary Information for the foregoing purpose.


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
419
```

</details>

<details><summary><code>span_text</code></summary>

```
4. Vendor and Ingram mutually agree that Ingram's public disclosure of the Proprietary Information, except pursuant to a confidential disclosure agreement, to any party will release Vendor from the obligation of confidentiality with respect to that portion of the Proprietary Information actually disclosed by Ingram.
```

</details>


---

## Audit questions

**Q1 — Naturalness (1–5).** Does this hardened task still look like a natural operator problem? See `PROTOCOL.md`.

**Q2 — Verifier validity.** Would the verifier rule above accept the same outputs you would accept on this task? Choose `agree`, `disagree_too_strict`, `disagree_too_lax`, or `disagree_other`.

Append your answer to your responses file under the key `"contract:419/hypothesis:nda-7/span:16"`. See `responses/EXAMPLE_filled.json`.
