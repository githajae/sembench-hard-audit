# Audit task — contractnli / map

**task_key:** `contract:437/hypothesis:nda-20`  
**task_family:** `hard_map`  
**file stem:** `18_map_contract_437_hypothesis_nda-20`

> Read this page top-to-bottom, then write your two ratings into `responses/<your_name>.json` under the key shown above. See `PROTOCOL.md` for the rubric.

---

## Key facts

*(The inputs the model would see, plus the gold answer with span / sentence ids resolved to their text. These are the facts you actually need to rate Q1 and Q2.)*

**Hypothesis** (the claim about the contract):

> Receiving Party may retain some Confidential Information even after the return or destruction of Confidential Information.

**Gold label:** `contradiction`

**Gold-evidence variants** (each variant is one accepted set of `span_ids`; the verifier accepts any single variant exactly):

- Variant 1: `span_ids = [41]`
  > In the event an employee of Recipient terminates his or her employment with Recipient, Recipient agrees to require such terminated employee to immediately return to Recipient all copies of the Confidential Information in such employee's possession at the time of termination of employment.


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
437
```

</details>

<details><summary><code>contract_text</code> (truncated)</summary>

```
[SPAN 25] Company and Client agree to permit Recipient to have access to the Confidential Information as requested herein by Client, but only in accordance with the terms of this Agreement.
[SPAN 28] Company and Client hereby agree to permit Recipient to have access to the Confidential Information listed below for the sole purpose of assisting Client with the Conversion, and such access is granted solely upon the terms and conditions set forth in this Agreement. 
[SPAN 36] Recipient acknowledges that the Application Software and all documentation and related materials are proprietary to Company and are confidential and constitute a valuable asset of Company, and that the data files contained in the Confidential Information are proprietary to Client and are confidential and constitute a valuable asset of Client. 
[SPAN 37] Recipient agrees to safeguard the Confidential Information, and Recipient shall not disclose or give access to the Confidential Information to any person or entity other than those employees of Recipient who have a need for such access in order to assist Client with Conversion.
[SPAN 38] 3. Unauthorized Use. Recipient shall not make any unauthorized use or disclosure of the Confidential Information and Recipient shall promptly advise Company and Client in writing if Recipient learns of any unauthorized use or disclosure of the Confidential Information or Application Software by anyone, whether an employee, former employee or agent of Recipient, or others, an
... [truncated, full content in the .json file] ...
```

</details>

<details><summary><code>inventory_span_ids</code></summary>

```
[
  25,
  28,
  36,
  37,
  38,
  39,
  41,
  43,
  44,
  46
]
```

</details>


---

## Audit questions

**Q1 — Naturalness (1–5).** Does this hardened task still look like a natural operator problem? See `PROTOCOL.md`.

**Q2 — Verifier validity.** Would the verifier rule above accept the same outputs you would accept on this task? Choose `agree`, `disagree_too_strict`, `disagree_too_lax`, or `disagree_other`.

Append your answer to your responses file under the key `"contract:437/hypothesis:nda-20"`. See `responses/EXAMPLE_filled.json`.
