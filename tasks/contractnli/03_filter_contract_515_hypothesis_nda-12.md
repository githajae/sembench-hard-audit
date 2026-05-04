# Audit task — contractnli / filter

**task_key:** `contract:515/hypothesis:nda-12`  
**task_family:** `hard_filter`  
**file stem:** `03_filter_contract_515_hypothesis_nda-12`

> Read this page top-to-bottom, then write your two ratings into `responses/<your_name>.json` under the key shown above. See `PROTOCOL.md` for the rubric.

---

## Key facts

*(The inputs the model would see, plus the gold answer with span / sentence ids resolved to their text. These are the facts you actually need to rate Q1 and Q2.)*

**Hypothesis** (the claim about the contract):

> Receiving Party may independently develop information similar to Confidential Information.

**Gold label:** `entailment`

**Gold-evidence variants** (each variant is one accepted set of `span_ids`; the verifier accepts any single variant exactly):

- Variant 1: `span_ids = [27, 30]`
  > Confidential Information shall not include information that:
  > (iii) is independently developed after the Employee’s termination of employment without reference to or use of the Confidential Information or materials based thereon;

**Confuser / candidate clauses (first 5 shown in full):**

- `span_id = 44` — In addition, Employee has or may develop relationships with Customers or Potential Customers so that the Confidential Information could be used to Solicit the business of such Customer or Potential Customer away from a Banking Organization.
- `span_id = 11` — WHEREAS, as a result of employment with Heritage up to the Effective Time and with the Bank thereafter, Employee had, has and will have access to Confidential Information (as defined below) and may have acquired or will acquire knowledge regarding Confidential Information, including, but not limited to, information regarding Customers or Potential Customers (as defined below), and a Banking Organization could be harmed if such Confidential Information were to be used, divulged or become known to any competitor of a Banking Organization or to any other Person (as defined below) or to any entity
- `span_id = 63` — c. performing or supervising those that perform data processing, accounting, rate review, document review or similar “back room” services related to a Customer or Potential Customer so long as the services do not require the disclosure of Confidential Information or contact with the Customer or Potential Customer.
- `span_id = 123` — Employee further represents that he/she has not retained any documents or information relating to Employee’s prior employers (other than Heritage or HopFed) that may be considered confidential or proprietary information and that Employee has not disclosed or used, and will not disclose or use, any information relating to his or her prior employer(s) in connection with Employee’s employment with a Financial Institution.
- `span_id = 45` — Employee shall not, directly or indirectly, use any Confidential Information for any purpose other than the benefit of a Banking Organization, and shall not directly or indirectly, disclose, communicate, deliver, exhibit or provide any Confidential Information to any Person, except other Employees or Agents of a Banking Organization who have a need to know such Confidential Information for a proper corporate or business purpose, as required in the normal course of Employee’s service as an employee.


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
515
```

</details>

<details><summary><code>contract_text</code> (truncated)</summary>

```
Exhibit 10.8
NON-DISCLOSURE AND NON-SOLICITATION AGREEMENT
THIS NON-DISCLOSURE AND NON-SOLICITATION AGREEMENT (“Agreement”) is made and entered into, effective as of the date first written below, by and among First Financial Corporation (“First Financial”), First Financial Bank, N.A. (“Bank”), a wholly-owned subsidiary of First Financial, HopFed Bancorp, Inc. (“HopFed”), Heritage Bank USA, Inc., (“Heritage”), a wholly-owned subsidiary of HopFed, and Billy C. Duvall (“Employee”). “Banking Organization” shall mean First Financial, the Bank, HopFed, and/or Heritage. “Financial Institution” shall mean the Bank and/or Heritage. First Financial, the Bank, HopFed, Heritage and Employee may be collectively referenced as the “parties” or individually as a “party.”
WHEREAS, pursuant to that certain Agreement and Plan of Merger, dated January 7, 2019, by and between HopFed and First Financial (the “Merger Agreement”), HopFed shall be merged with and into First Financial (the “Merger”) effective as of the date and time provided in the Merger Agreement (the “Effective Time”); and
WHEREAS, Heritage will be merged into the Bank at the Effective Time or shortly thereafter; and
WHEREAS, Employee is currently an employee of Heritage and the Bank intends to offer employment to the Employee as an at-will employee to provide services for and on behalf of the Bank immediately upon the Effective Time;
WHEREAS, as a result of employment with Heritage up to the Effective Time and with the Bank therea
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

Append your answer to your responses file under the key `"contract:515/hypothesis:nda-12"`. See `responses/EXAMPLE_filled.json`.
