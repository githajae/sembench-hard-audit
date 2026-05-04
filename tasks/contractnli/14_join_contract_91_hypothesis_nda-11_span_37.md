# Audit task — contractnli / join

**task_key:** `contract:91/hypothesis:nda-11/span:37`  
**task_family:** `hard_join`  
**file stem:** `14_join_contract_91_hypothesis_nda-11_span_37`

> Read this page top-to-bottom, then write your two ratings into `responses/<your_name>.json` under the key shown above. See `PROTOCOL.md` for the rubric.

---

## Key facts

*(The inputs the model would see, plus the gold answer with span / sentence ids resolved to their text. These are the facts you actually need to rate Q1 and Q2.)*

**Hypothesis** (the claim about the contract):

> Receiving Party shall not reverse engineer any objects which embody Disclosing Party's Confidential Information.

**Candidate clause** (`span_id = 37`):

> IV. NO REVERSE ENGINEERING; WORK PRODUCT: Receiving Party shall not reverse-engineer, analyze, attempt to duplicate or otherwise attempt to determine the design or method of compiling samples, prototypes or products of the Originating Party except pursuant to a mutually acceptable, written agreement executed by the parties.

**Gold label:** `evidence`

**Confuser / candidate clauses (first 5 shown in full):**

- `span_id = 24` — 13. “Confidential Information” shall not include information which, now or in the future, is available to the public (other than through improper disclosure by the Receiving Party); information rightly acquired from a third party without any obligation of confidentiality; information that is independently developed without the use of any Confidential Information; or information already known by Receiving Party prior to disclosure by Originating Party, as demonstrated by written evidence.
- `span_id = 10` — A. “Confidential Information” as used herein any and all confidential and/or proprietary information concerning the Originating Party’s business and such party’s trade secrets, proprietary data and business data, whether oral or written, tangible or intangible, which is disclosed to or learned by the Receiving Party in the course of the Discussions or otherwise while working with the Originating Party, and/or discovered, developed, conceived, originated, appreciably modified, or prepared in scope of Receiving Party’s relationship with the Originating Party, including but not limited to the fol
- `span_id = 35` — III. LEGALLY REQUIRED DISCLOSURES: If Receiving Party is requested to disclose any Confidential Information of the Originating Party under applicable law, in any judicial or administrative proceeding, or in response to a formal request of a regulatory or governmental authority (including law enforcement), then, except as otherwise required to comply with applicable law, the Receiving Party shall promptly notify the Originating Party of such request so that Originating Party may resist such disclosure or seek an appropriate protective order, and shall provide all information and assistance reas
- `span_id = 29` — II. NON-DISCLOSURE AGREEMENT: Both parties recognizes and acknowledges that, in an effort to foster the Discussions one or both of the parties has provided and/or will provide, at no cost, fee, charge or expense to Receiving Party, Confidential Information of a special and unique value and nature developed and/or acquired by (and/or being developed or acquired by) Originating Party at great expense and cost to Originating Party which, if it were to come into the possession of Originating Party’s competitors, would cause irreparable damage to Originating Party, its competitive advantage and its
- `span_id = 5` — WHEREAS, Dealer Pay and COMPANY desire to explore the possibility of entering into one or more potential business transactions or relationships (each a “Business Relationship”), with the understanding that any such Business Relationship would be embodied in a mutually acceptable, definitive written agreement executed by the parties; and


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
91
```

</details>

<details><summary><code>span_text</code></summary>

```
IV. NO REVERSE ENGINEERING; WORK PRODUCT: Receiving Party shall not reverse-engineer, analyze, attempt to duplicate or otherwise attempt to determine the design or method of compiling samples, prototypes or products of the Originating Party except pursuant to a mutually acceptable, written agreement executed by the parties. 
```

</details>


---

## Audit questions

**Q1 — Naturalness (1–5).** Does this hardened task still look like a natural operator problem? See `PROTOCOL.md`.

**Q2 — Verifier validity.** Would the verifier rule above accept the same outputs you would accept on this task? Choose `agree`, `disagree_too_strict`, `disagree_too_lax`, or `disagree_other`.

Append your answer to your responses file under the key `"contract:91/hypothesis:nda-11/span:37"`. See `responses/EXAMPLE_filled.json`.
