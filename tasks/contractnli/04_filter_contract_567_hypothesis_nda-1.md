# Audit task — contractnli / filter

**task_key:** `contract:567/hypothesis:nda-1`  
**task_family:** `hard_filter`  
**file stem:** `04_filter_contract_567_hypothesis_nda-1`

> Read this page top-to-bottom, then write your two ratings into `responses/<your_name>.json` under the key shown above. See `PROTOCOL.md` for the rubric.

---

## Key facts

*(The inputs the model would see, plus the gold answer with span / sentence ids resolved to their text. These are the facts you actually need to rate Q1 and Q2.)*

**Hypothesis** (the claim about the contract):

> All Confidential Information shall be expressly identified by the Disclosing Party.

**Gold label:** `contradiction`

**Gold-evidence variants** (each variant is one accepted set of `span_ids`; the verifier accepts any single variant exactly):

- Variant 1: `span_ids = [14]`
  > “Confidential Information” shall mean any information belonging to a party or a related company (as hereinafter defined) which is not generally available to or used by others, or the utility or value of which is not generally known or recognized as a standard practice and may include without limitation any and all financial information; any and all employment information; any and all technical and non-technical information, including patent, copyright, trade secret and similar proprietary information; any information related to current, future and proposed business information, plans, activities, products and services, computer software, and other technology, including without limitation, forecasts, market research, development, design details, specifications, financial information, procurement requirements, purchasing, manufacturing, contractor and subcontractor lists, and sales and merchandising plans (including such information of each and any affiliate, subsidiary, or the like) in any medium whatsoever, whether oral, written, machine readable data, through facsimile, electronic mail, postal service or otherwise, provided by or disclosed either directly or indirectly by the Disclosing Party to the Receiving Party whether such information is designated as confidential at the time of delivery or not.

**Confuser / candidate clauses (first 5 shown in full):**

- `span_id = 39` — The Confidential Information, and all rights thereto, which have been or will be disclosed to one of the parties shall remain the exclusive property of the Disclosing Party and shall he held in confidence by the Receiving Party for the other.
- `span_id = 62` — Each party shall immediately upon the Termination of this Agreement or at any time upon the request of the Disclosing Party, discontinue use of the Confidential Information of the other and, if requested by the Disclosing Party, return same and all copies thereof which may be or
- `span_id = 64` — If return is not requested, the Confidential Information shall be destroyed within ten (10) Business Days of the Termination of the Agreement and an officer’s certificate to that effect provided by the Disclosing Party.
- `span_id = 42` — Each party shall only have the right to disclose the Confidential Information to its employees, agents and consultants on a “need to know” basis; provided, however, that disclosure in any event shall only be made to such persons who have agreed in writing to protect the confidentiality of the Disclosing Party’s information.
- `span_id = 87` — Each party acknowledges that, notwithstanding the execution of the Agreement, each Disclosing Party maintains the sole and absolute discretion to determine what, if any, of its Confidential Information shall be disclosed to the Receiving Party.


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
567
```

</details>

<details><summary><code>contract_text</code> (truncated)</summary>

```
Mutual Non-Disclosure Agreement
This Agreement is made as of the 30th day of May, 2008 between e-Smart technologies, Inc., and all of its subsidiaries and affiliates acting through its offices located at 526 W. 26th St./Ste. 710, New York, N.Y. 10001 (“E-SMART”), and “Lee&Pak,.Ltd”, a Korean corporation, and all of its subsidiaries and affiliates acting through its offices located at 1599-2 LG Edat Bldg 9th FI., Seocho-dong, Seocho-Gu, Seoul, Korea (“LEE&PAK”).
BACKGROUND:
1. For the limited and sole purpose, of evaluating E-SMART’s business and LEE&PAK’s technology in contemplation of a potential to be agreed, mutually acceptable business arrangement, it is contemplated that each of LEE&PACK will require access to certain Confidential Information, as hereinafter defined, of the other.
2. Each party wishes to protect the confidentiality of its Confidential Information that may be disclosed hereunder.
IN CONSIDERATION of the background and the mutual covenants and agreements herein contained, the parties hereto agree as follows:
ARTICLE 1
INTERPRETATION
1.01 Definitions. In this Agreement, unless something in the subject matter or context is inconsistent therewith:
“Agreement” means this Agreement and all amendments made hereto by written agreement between LEE&PAK and E-SMART.
“Business Day” means any day except Saturday, Sunday and statutory holidays observed in the Country of Korea.
“Disclosing Party” is the party who is disclosing Confidential Information to the other party
... [truncated, full content in the .json file] ...
```

</details>

<details><summary><code>document_type</code></summary>

```
sec-html
```

</details>


---

## Audit questions

**Q1 — Naturalness (1–5).** Does this hardened task still look like a natural operator problem? See `PROTOCOL.md`.

**Q2 — Verifier validity.** Would the verifier rule above accept the same outputs you would accept on this task? Choose `agree`, `disagree_too_strict`, `disagree_too_lax`, or `disagree_other`.

Append your answer to your responses file under the key `"contract:567/hypothesis:nda-1"`. See `responses/EXAMPLE_filled.json`.
