# Audit task — contractnli / join

**task_key:** `contract:505/hypothesis:nda-12/span:31`  
**task_family:** `hard_join`  
**file stem:** `10_join_contract_505_hypothesis_nda-12_span_31`

> Read this page top-to-bottom, then write your two ratings into `responses/<your_name>.json` under the key shown above. See `PROTOCOL.md` for the rubric.

---

## Key facts

*(The inputs the model would see, plus the gold answer with span / sentence ids resolved to their text. These are the facts you actually need to rate Q1 and Q2.)*

**Hypothesis** (the claim about the contract):

> Receiving Party may independently develop information similar to Confidential Information.

**Candidate clause** (`span_id = 31`):

> Notwithstanding the foregoing, the definition of Confidential Information shall not include any of the foregoing items insofar as they relate to Seller Exclusive Products.

**Gold label:** `not_evidence`

**Confuser / candidate clauses (first 5 shown in full):**

- `span_id = 54` — Seller hereby agrees that, during the Restricted Period, except as permitted by Section 5 of this Agreement, Seller will not, directly or indirectly, solicit, induce or influence any customer, supplier, lender, lessor or any other Person that has a business relationship with the Business in the Protected Market, or which had on the date of this Agreement a business relationship with the Business in the Protected Market, to discontinue or reduce the extent of such relationship with the Business in the Protected Market; it being understood that, nothing herein shall restrict Seller from carrying
- `span_id = 57` — Seller hereby agrees that, during the Restricted Period, it will not, directly or indirectly, disclose to anyone, or use or otherwise exploit for its own benefit or for the benefit of anyone other than Purchaser, any Confidential Information, except as permitted by Section 5 of this Agreement.
- `span_id = 51` — Seller hereby agrees that, during the Restricted Period, except as permitted by Section 5 of this Agreement, it will not, directly or indirectly, own, manage, operate, control, invest in or acquire an interest in, or otherwise engage or participate in the establishment, management or operation of, any Competitive Business that sells or distributes Competitive Products, directly or indirectly, for ultimate purchase by consumers in the Protected Market, without regard to whether the Competitive Business has any office, manufacturing or other business facilities within the Protected Market.
- `span_id = 24` — (b) “Competitive Products” shall mean the type of products designed, marketed, imported, and sold or distributed by Seller to the Infant and Toddler Retail Market in connection with the operation of the Business prior to the date hereof (which shall not include
- `span_id = 48` — (i) “Seller Exclusive Products” means any Inventory (as defined in the Purchase Agreement) that is not included within the Eligible Inventory (as defined in the Purchase Agreement) transferred to Purchaser pursuant to the Purchase Agreement.


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
505
```

</details>

<details><summary><code>span_text</code></summary>

```
Notwithstanding the foregoing, the definition of Confidential Information shall not include any of the foregoing items insofar as they relate to Seller Exclusive Products.
```

</details>


---

## Audit questions

**Q1 — Naturalness (1–5).** Does this hardened task still look like a natural operator problem? See `PROTOCOL.md`.

**Q2 — Verifier validity.** Would the verifier rule above accept the same outputs you would accept on this task? Choose `agree`, `disagree_too_strict`, `disagree_too_lax`, or `disagree_other`.

Append your answer to your responses file under the key `"contract:505/hypothesis:nda-12/span:31"`. See `responses/EXAMPLE_filled.json`.
