# Audit task — contractnli / map

**task_key:** `contract:391/hypothesis:nda-1`  
**task_family:** `hard_map`  
**file stem:** `17_map_contract_391_hypothesis_nda-1`

> Read this page top-to-bottom, then write your two ratings into `responses/<your_name>.json` under the key shown above. See `PROTOCOL.md` for the rubric.

---

## Key facts

*(The inputs the model would see, plus the gold answer with span / sentence ids resolved to their text. These are the facts you actually need to rate Q1 and Q2.)*

**Hypothesis** (the claim about the contract):

> All Confidential Information shall be expressly identified by the Disclosing Party.

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
391
```

</details>

<details><summary><code>contract_text</code> (truncated)</summary>

```
[SPAN 57] Notwithstanding the foregoing, CompuCom shall be permitted to provide Services under any "request for proposal", bid, contract or statement of work submitted by CompuCom to the applicable potential customer prior to May 12, 1999 . 
[SPAN 77] Seller shall be permitted to disclose historical financial information, including financial information relating to the Business, as may be required by customers, vendors, lenders or other third parties, provided that such third parties shall agree to preserve the confidentiality of such information.
[SPAN 83] (a) CompuCom shall cooperate with Seller at Seller's expense to protect and safeguard all of Seller's Confidential Information;
[SPAN 86] As used in this Agreement, the terms "Seller's Confidential Information" means proprietary or confidential information and business secrets of Seller pertaining to its Services Business including, without limitation, information regarding prices charged for Services, copies of existing Services contracts to which Seller is a party (other than any such contracts provided to CompuCom pursuant to the provisions of the Asset Purchase Agreement) and analyses of the amount and types of Services purchased by customers.
[SPAN 90] All notices, requests, demands or other communications required by or otherwise with respect to this Agreement shall be in writing and shall be deemed to have been duly given to any party when delivered personally (by courier service or otherwise), when delivered by fac
... [truncated, full content in the .json file] ...
```

</details>

<details><summary><code>inventory_span_ids</code></summary>

```
[
  57,
  77,
  83,
  86,
  90,
  126,
  134,
  136,
  138,
  141
]
```

</details>


---

## Audit questions

**Q1 — Naturalness (1–5).** Does this hardened task still look like a natural operator problem? See `PROTOCOL.md`.

**Q2 — Verifier validity.** Would the verifier rule above accept the same outputs you would accept on this task? Choose `agree`, `disagree_too_strict`, `disagree_too_lax`, or `disagree_other`.

Append your answer to your responses file under the key `"contract:391/hypothesis:nda-1"`. See `responses/EXAMPLE_filled.json`.
