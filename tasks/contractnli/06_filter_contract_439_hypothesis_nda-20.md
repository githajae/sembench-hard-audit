# Audit task — contractnli / filter

**task_key:** `contract:439/hypothesis:nda-20`  
**task_family:** `hard_filter`  
**file stem:** `06_filter_contract_439_hypothesis_nda-20`

> Read this page top-to-bottom, then write your two ratings into `responses/<your_name>.json` under the key shown above. See `PROTOCOL.md` for the rubric.

---

## Key facts

*(The inputs the model would see, plus the gold answer with span / sentence ids resolved to their text. These are the facts you actually need to rate Q1 and Q2.)*

**Hypothesis** (the claim about the contract):

> Receiving Party may retain some Confidential Information even after the return or destruction of Confidential Information.

**Gold label:** `contradiction`

**Gold-evidence variants** (each variant is one accepted set of `span_ids`; the verifier accepts any single variant exactly):

- Variant 1: `span_ids = [30, 31]`
  > Upon the termination of this Agreement, Recipient shall promptly return to MS.
  > or certify destruction of, all full or partial copies of the Product and related materials provided by MS.

**Confuser / candidate clauses (first 5 shown in full):**

- `span_id = 41` — Recipient agrees not to disclose or provide the Product, documentation, or any related information (including the Product features or the results of use or testing) to any third party or use the Product for any purpose other than as provided in this Agreement.
- `span_id = 57` — BECAUSE SOME STATES/JURISDICTIONS DO NOT ALLOW THE EXCLUSION OR LIMITATION OF LIABILITY FOR CONSEQUENTIAL OR INCIDENTAL DAMAGES, THE ABOVE LIMITATION MAY NOT APPLY TO RECIPIENT.
- `span_id = 4` — MS may, in its sole discretion, also provide further pre-releases of the Product or related information to Recipient hereunder, in which case such further pre-releases and related information shall also be covered hereunder as "Product".
- `span_id = 3` — Upon receipt by Microsoft Corporation ("MS") of this Agreement, signed and completed by the individual or organization indicated below ("Recipient"), MS may elect, at MS' sole discretion, to provide Recipient with a pre-release copy of the MS product MSN Software Development Kit, and related documentation and information (collectively the "Product").
- `span_id = 42` — However, Recipient may disclose confidential information in accordance with judicial or other governmental order, provided Recipient shall give MS reasonable written notice prior to such disclosure and shall comply with any applicable protective order or equivalent.


---

## Verifier rule (what the strict verifier checks)

> Output is `(label, span_ids)` over the contract. Accept iff `label` matches the gold (`entailment` / `contradiction` / `not_mentioned`) AND `span_ids` equals one of the accepted gold-evidence variants. Empty `span_ids` only valid for `not_mentioned`.

This rule is the contract you are auditing in **Q2**.

---

## Policy / instructions (as the model sees them)

> Use the full contract and return the final label together with the exact span ids that directly determine it under exception-sensitive reasoning. If the hypothesis is not mentioned, return not_mentioned and an empty span_ids list.

---

## Other fields (collapsed, for reference)

<details><summary><code>contract_id</code></summary>

```
439
```

</details>

<details><summary><code>contract_text</code> (truncated)</summary>

```
MICROSOFT CORPORATION NON-DISCLOSURE AGREEMENT
(PRE-RELEASE PRODUCT-GENERAL)
IMPORTANT: PLEASE COMPLETE THIS FORM AND RETURN IT TO MICROSOFT AT THE ADDRESS BELOW:
Upon receipt by Microsoft Corporation ("MS") of this Agreement, signed and completed by the individual or organization indicated below ("Recipient"), MS may elect, at MS' sole discretion, to provide Recipient with a pre-release copy of the MS product MSN Software Development Kit, and related documentation and information (collectively the "Product"). MS may, in its sole discretion, also provide further pre-releases of the Product or related information to Recipient hereunder, in which case such further pre-releases and related information shall also be covered hereunder as "Product".
1, GRANT OF LICENSE.
(a) MS grants to Recipient a limited, non-exclusive, nontransferable, royalty-free license to use up to five copies of the executable Product code on CPU's residing at Recipient's premises solely to test the compatibility of Recipient's application or other product(s) ("Application") which operate in conjunction with the Product and to evaluate the Product for the purpose of providing feedback thereon to MS. All other rights are reserved to MS. Recipient shall not rent, lease, sell, sublicense, assign, or otherwise transfer the Product, including any accompanying printed materials. Recipient may not reverse engineer, decompile or disassemble the Product except to the extent that this restriction is expressly prohibi
... [truncated, full content in the .json file] ...
```

</details>

<details><summary><code>document_type</code></summary>

```
sec-text
```

</details>


---

## Audit questions

**Q1 — Naturalness (1–5).** Does this hardened task still look like a natural operator problem? See `PROTOCOL.md`.

**Q2 — Verifier validity.** Would the verifier rule above accept the same outputs you would accept on this task? Choose `agree`, `disagree_too_strict`, `disagree_too_lax`, or `disagree_other`.

Append your answer to your responses file under the key `"contract:439/hypothesis:nda-20"`. See `responses/EXAMPLE_filled.json`.
