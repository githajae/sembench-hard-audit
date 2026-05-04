# Audit task — contractnli / filter

**task_key:** `contract:386/hypothesis:nda-1`  
**task_family:** `hard_filter`  
**file stem:** `02_filter_contract_386_hypothesis_nda-1`

> Read this page top-to-bottom, then write your two ratings into `responses/<your_name>.json` under the key shown above. See `PROTOCOL.md` for the rubric.

---

## Key facts

*(The inputs the model would see, plus the gold answer with span / sentence ids resolved to their text. These are the facts you actually need to rate Q1 and Q2.)*

**Hypothesis** (the claim about the contract):

> All Confidential Information shall be expressly identified by the Disclosing Party.

**Gold label:** `entailment`

**Gold-evidence variants** (each variant is one accepted set of `span_ids`; the verifier accepts any single variant exactly):

- Variant 1: `span_ids = [15]`
  > 4. EMPLOYEE further agrees not to divulge to any third party, either during his or her employment or thereafter, any confidential information conceived by him or her, disclosed by FRANKLIN, or obtained by him or her while in the employment of FRANKLIN relating in any way to any of FRANKLIN'S processes, businesses, customers, trade secrets, apparatus, products, software, packages, programs or trends in research, or to any of the inventions, discoveries, writings, programs, and improvements covered hereby, and agrees to maintain this information in confidence until such time that such information has become widely known to the public or described in an issued patent or in a printed publication of wide circulation.

**Confuser / candidate clauses (first 5 shown in full):**

- `span_id = 16` — Upon termination of the employment, EMPLOYEE agrees to turn over to FRANKLIN all notes, memoranda, notebooks, drawings, records, customer lists, telephone files (including Rolodex and business card files) and correspondence in connection with anything done by him or her relating to his or her employment, for the reason that all confidential information contained therein is at all times the sole property of FRANKLIN.
- `span_id = 14` — 3. EMPLOYEE shall from time to time, upon request of FRANKLIN execute all papers and do all other things that may be reasonably required in order to protect the rights of FRANKLIN, and to vest in FRANKLIN or its successors or assigns the entire rights, title and interest in and to any and all inventions, discoveries, writings, program improvements, and applications for letters patent or copyright or maskwork registrations relating to anything pertaining to or useful in the business of FRANKLIN as provided above.
- `span_id = 12` — 1. EMPLOYEE shall promptly and fully disclose to FRANKLIN any and all inventions, discoveries, writings, programs, and improvements made by him or her pertaining to or useful in the business of FRANKLIN during his or her period of employment by FRANKLIN, and any improvements to his or her invention, writings, programs, and discoveries, made, conceived or acquired by him or her no later than one year after the termination of employment, whether made or conceived solely or jointly with others, whether during regular business hours or otherwise; said Inventions, discoveries, writings, programs or
- `span_id = 13` — 2. EMPLOYEE shall from time to time, upon request and at the expense of FRANKLIN, make application through the attorneys for FRANKLIN for any letters patent or copyright or maskwork registrations of the United States, and any and all foreign countries, on said inventions, discoveries, writings, programs or improvements, and assign and transfer all said applications, inventions, discoveries, writings, programs, and improvements to FRANKLIN or its nominee, without further consideration.
- `span_id = 8` — 1. EMPLOYEE has been hired by FRANKLIN in a position with access to information relating to the understanding of, testing, or improvement of existing products of FRANKLIN, the development of new products for FRANKLIN, and/or the general business activities of FRANKLIN.


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
386
```

</details>

<details><summary><code>contract_text</code> (truncated)</summary>

```
PATENT ASSIGNMENT AND NON-DISCLOSURE AGREEMENT
AGREEMENT between FRANKLIN ELECTRONIC PUBLISHERS, INC., a Pennsylvania corporation, having a place of business at One Franklin Plaza, Burlington, New Jersey 08016-4907 or any of its subsidiaries (referred to as "FRANKLIN") and ____________________________ residing at ________________________ an employee of Franklin or one of its subsidiaries ("EMPLOYEE").
BACKGROUND
1. EMPLOYEE has been hired by FRANKLIN in a position with access to information relating to the understanding of, testing, or improvement of existing products of FRANKLIN, the development of new products for FRANKLIN, and/or the general business activities of FRANKLIN.
2. The parties desire to reduce to writing the patent assignment and non-disclosure aspects of the employment relationship.
TERMS OF AGREEMENT
In and for the consideration of the employment of EMPLOYEE by FRANKLIN, EMPLOYEE agrees as follows:
1. EMPLOYEE shall promptly and fully disclose to FRANKLIN any and all inventions, discoveries, writings, programs, and improvements made by him or her pertaining to or useful in the business of FRANKLIN during his or her period of employment by FRANKLIN, and any improvements to his or her invention, writings, programs, and discoveries, made, conceived or acquired by him or her no later than one year after the termination of employment, whether made or conceived solely or jointly with others, whether during regular business hours or otherwise; said Inventions, disco
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

Append your answer to your responses file under the key `"contract:386/hypothesis:nda-1"`. See `responses/EXAMPLE_filled.json`.
