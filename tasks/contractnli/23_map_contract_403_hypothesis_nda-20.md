# Audit task — contractnli / map

**task_key:** `contract:403/hypothesis:nda-20`  
**task_family:** `hard_map`  
**file stem:** `23_map_contract_403_hypothesis_nda-20`

> Read this page top-to-bottom, then write your two ratings into `responses/<your_name>.json` under the key shown above. See `PROTOCOL.md` for the rubric.

---

## Key facts

*(The inputs the model would see, plus the gold answer with span / sentence ids resolved to their text. These are the facts you actually need to rate Q1 and Q2.)*

**Hypothesis** (the claim about the contract):

> Receiving Party may retain some Confidential Information even after the return or destruction of Confidential Information.

**Gold label:** `contradiction`

**Gold-evidence variants** (each variant is one accepted set of `span_ids`; the verifier accepts any single variant exactly):

- Variant 1: `span_ids = [23]`
  > At any time upon NIM's request, Seller shall turn over to NIM all books, notes, memoranda, manuals, notebooks, records and other documents made, compiled by, delivered to, or in the possession or control of Seller containing or concerning any Confidential Information, including all copies thereof, in any form or format, including any computer hard disks containing Confidential Information, wherever located, containing any such information, it being agreed that the same and all information contained therein are at all times the exclusive property of NIM and its Affiliates; provided, however, in the event that computer hard disks contain Confidential Information as well as information confidential to the Seller, then Seller shall make copies of all Confidential Information on such computer hard disks and return such copies to NIM and delete the Confidential Information from such computer hard disks.


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
403
```

</details>

<details><summary><code>contract_text</code> (truncated)</summary>

```
[SPAN 11] (A) Engage in the business of providing record-keeping and administrative services for retirement plans and sales of insurance products to clients of third party administrators (the "Restricted Business") anywhere in the Territory (as defined below), or be employed by, engage or participate in the ownership, management, operation or control of, or act in any advisory, expert, consulting or other capacity for, any entity or individual engaged in the Restricted Business anywhere in the geographical area within the United States (the "Territory");
[SPAN 21] Seller understands and agrees that the business of NIM and its Affiliates is based upon specialized work and Confidential Information (as hereinafter defined). 
[SPAN 22] Seller agrees that following the termination of Seller's employment or consulting period with NIM or any Affiliate of NIM and for all times thereafter, he shall keep secret all such Confidential Information and that he will not, directly or indirectly, use for his own benefit or for the benefit of others nor Disclose (as hereinafter defined), without the prior written consent of NIM, any Confidential Information. 
[SPAN 23] At any time upon NIM's request, Seller shall turn over to NIM all books, notes, memoranda, manuals, notebooks, records and other documents made, compiled by, delivered to, or in the possession or control of Seller containing or concerning any Confidential Information, including all copies thereof, in any form or format, includin
... [truncated, full content in the .json file] ...
```

</details>

<details><summary><code>inventory_span_ids</code></summary>

```
[
  11,
  21,
  22,
  23,
  24,
  27,
  29,
  30,
  36,
  51
]
```

</details>


---

## Audit questions

**Q1 — Naturalness (1–5).** Does this hardened task still look like a natural operator problem? See `PROTOCOL.md`.

**Q2 — Verifier validity.** Would the verifier rule above accept the same outputs you would accept on this task? Choose `agree`, `disagree_too_strict`, `disagree_too_lax`, or `disagree_other`.

Append your answer to your responses file under the key `"contract:403/hypothesis:nda-20"`. See `responses/EXAMPLE_filled.json`.
