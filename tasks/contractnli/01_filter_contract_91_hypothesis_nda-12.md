# Audit task — contractnli / filter

**task_key:** `contract:91/hypothesis:nda-12`  
**task_family:** `hard_filter`  
**file stem:** `01_filter_contract_91_hypothesis_nda-12`

> Read this page top-to-bottom, then write your two ratings into `responses/<your_name>.json` under the key shown above. See `PROTOCOL.md` for the rubric.

---

## Key facts

*(The inputs the model would see, plus the gold answer with span / sentence ids resolved to their text. These are the facts you actually need to rate Q1 and Q2.)*

**Hypothesis** (the claim about the contract):

> Receiving Party may independently develop information similar to Confidential Information.

**Gold label:** `entailment`

**Gold-evidence variants** (each variant is one accepted set of `span_ids`; the verifier accepts any single variant exactly):

- Variant 1: `span_ids = [24]`
  > 13. “Confidential Information” shall not include information which, now or in the future, is available to the public (other than through improper disclosure by the Receiving Party); information rightly acquired from a third party without any obligation of confidentiality; information that is independently developed without the use of any Confidential Information; or information already known by Receiving Party prior to disclosure by Originating Party, as demonstrated by written evidence.

**Confuser / candidate clauses (first 5 shown in full):**

- `span_id = 35` — III. LEGALLY REQUIRED DISCLOSURES: If Receiving Party is requested to disclose any Confidential Information of the Originating Party under applicable law, in any judicial or administrative proceeding, or in response to a formal request of a regulatory or governmental authority (including law enforcement), then, except as otherwise required to comply with applicable law, the Receiving Party shall promptly notify the Originating Party of such request so that Originating Party may resist such disclosure or seek an appropriate protective order, and shall provide all information and assistance reas
- `span_id = 32` — Representatives will at any time make any independent business or personal use of, retain, copy, divulge, disclose, reveal or communicate to any other person or organization (except as expressly authorized in writing by Originating Party, as required to analyze the Business Relationship or as required to fulfill Receiving Party’s obligations to Originating Party) any Confidential Information.
- `span_id = 26` — C. “Originating Party” as used herein shall refer to the party who discloses the Confidential Information or Intellectual Property to the Receiving Party.
- `span_id = 27` — D. “Receiving Party” as used herein shall refer to the party who receives the Confidential Information or Intellectual Property from the Originating Party.
- `span_id = 29` — II. NON-DISCLOSURE AGREEMENT: Both parties recognizes and acknowledges that, in an effort to foster the Discussions one or both of the parties has provided and/or will provide, at no cost, fee, charge or expense to Receiving Party, Confidential Information of a special and unique value and nature developed and/or acquired by (and/or being developed or acquired by) Originating Party at great expense and cost to Originating Party which, if it were to come into the possession of Originating Party’s competitors, would cause irreparable damage to Originating Party, its competitive advantage and its


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
91
```

</details>

<details><summary><code>contract_text</code> (truncated)</summary>

```
MUTUAL NON-DISCLOSURE AGREEMENT
This Mutual Non-Disclosure Agreement (“Agreement”) is made and entered into on the date signed below by and between
_________________________________ (hereinafter “COMPANY”) and Dealer Pay, LLC (hereinafter “Dealer Pay”).
RECITALS:
WHEREAS, Dealer Pay owns and/or controls certain proprietary and confidential intellectual property, namely, a point-of-sale software platform for the automotive industry; and
WHEREAS, Dealer Pay and COMPANY desire to explore the possibility of entering into one or more potential business transactions or relationships (each a “Business Relationship”), with the understanding that any such Business Relationship would be embodied in a mutually acceptable, definitive written agreement executed by the parties; and
WHEREAS, in connection with any Business Relationship and any discussions, demonstrations, evaluations and negotiations concerning a potential Business Relationship (“Discussions”), each party and/or its affiliates and/or their respective Representatives (as such term is defined below), may receive, observe and/or have physical or electronic access to certain Confidential Information (as defined below) of the other party and/or its affiliates; and
WHEREAS, Dealer Pay and COMPANY desire to ensure that appropriate confidentiality obligations are in place to protect Confidential Information from unauthorized access, use and disclosure.
NOW, THEREFORE, in consideration of the foregoing and the mutual covenants made
... [truncated, full content in the .json file] ...
```

</details>

<details><summary><code>document_type</code></summary>

```
search-pdf
```

</details>


---

## Audit questions

**Q1 — Naturalness (1–5).** Does this hardened task still look like a natural operator problem? See `PROTOCOL.md`.

**Q2 — Verifier validity.** Would the verifier rule above accept the same outputs you would accept on this task? Choose `agree`, `disagree_too_strict`, `disagree_too_lax`, or `disagree_other`.

Append your answer to your responses file under the key `"contract:91/hypothesis:nda-12"`. See `responses/EXAMPLE_filled.json`.
