# Audit task — contractnli / map

**task_key:** `contract:447/hypothesis:nda-17`  
**task_family:** `hard_map`  
**file stem:** `20_map_contract_447_hypothesis_nda-17`

> Read this page top-to-bottom, then write your two ratings into `responses/<your_name>.json` under the key shown above. See `PROTOCOL.md` for the rubric.

---

## Key facts

*(The inputs the model would see, plus the gold answer with span / sentence ids resolved to their text. These are the facts you actually need to rate Q1 and Q2.)*

**Hypothesis** (the claim about the contract):

> Receiving Party may create a copy of some Confidential Information in some circumstances.

**Gold label:** `contradiction`

**Gold-evidence variants** (each variant is one accepted set of `span_ids`; the verifier accepts any single variant exactly):

- Variant 1: `span_ids = [10, 12]`
  > 2. ALL NYNEX Confidential Information:
  > (b) shall not be copied, used, distributed, disclosed, disseminated or communicated in any way or form by CONSULTANT whether or not for its own benefit, to anyone outside or within its own organization, except on a "need-to-know" basis to the extent necessary for:


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
447
```

</details>

<details><summary><code>contract_text</code> (truncated)</summary>

```
[SPAN 4] WHEREAS, in order for CONSULTANT to provide consultant services to NYNEX it may be necessary or desirable for NYNEX to disclose to CONSULTANT certain confidential and proprietary material, information, data, and other communications concerning NYNEX's past, current, future and proposed or potential customers, products, services, operations, business forecasts, procurement requirements, plans strategies and technology; and
[SPAN 8] (a) disclosed by NYNEX and/or one or more of its parent, subsidiary or affiliated corporations, appropriately marked as "Confidential," "Proprietary" or the like or otherwise disclosed in a manner consistent with its proprietary and confidential nature; or 
[SPAN 10] 2. ALL NYNEX Confidential Information:
[SPAN 12] (b) shall not be copied, used, distributed, disclosed, disseminated or communicated in any way or form by CONSULTANT whether or not for its own benefit, to anyone outside or within its own organization, except on a "need-to-know" basis to the extent necessary for: 
[SPAN 18] (d) shall be held by CONSULTANT in the strictest confidence, and shall be treated by it with the same degree of care to avoid disclosure to any third party as is used with respect to CONSULTANT'S own information of like importance, or, a minimum, shall be treated with a reasonable degree of care to avoid any such disclosure. 
[SPAN 21] (e) Confidential Information is hereby acknowledged by CONSULTANT to be the sole property of NYNEX and shall be returned to N
... [truncated, full content in the .json file] ...
```

</details>

<details><summary><code>inventory_span_ids</code></summary>

```
[
  4,
  8,
  10,
  12,
  18,
  21,
  22,
  23,
  27,
  29
]
```

</details>


---

## Audit questions

**Q1 — Naturalness (1–5).** Does this hardened task still look like a natural operator problem? See `PROTOCOL.md`.

**Q2 — Verifier validity.** Would the verifier rule above accept the same outputs you would accept on this task? Choose `agree`, `disagree_too_strict`, `disagree_too_lax`, or `disagree_other`.

Append your answer to your responses file under the key `"contract:447/hypothesis:nda-17"`. See `responses/EXAMPLE_filled.json`.
