# Audit task — contractnli / filter

**task_key:** `contract:391/hypothesis:nda-18`  
**task_family:** `hard_filter`  
**file stem:** `08_filter_contract_391_hypothesis_nda-18`

> Read this page top-to-bottom, then write your two ratings into `responses/<your_name>.json` under the key shown above. See `PROTOCOL.md` for the rubric.

---

## Key facts

*(The inputs the model would see, plus the gold answer with span / sentence ids resolved to their text. These are the facts you actually need to rate Q1 and Q2.)*

**Hypothesis** (the claim about the contract):

> Receiving Party shall not solicit some of Disclosing Party's representatives.

**Gold label:** `entailment`

**Gold-evidence variants** (each variant is one accepted set of `span_ids`; the verifier accepts any single variant exactly):

- Variant 1: `span_ids = [35, 38, 51, 52, 53, 56, 81, 82, 85]`
  > (a) Seller agrees that during the Non-Competition Period Seller will not, and will not permit any of its Subsidiaries to:
  > (iii) solicit, entice or induce any employee of CompuCom or any Subsidiary of CompuCom to terminate his or her employment with CompuCom or any Subsidiary of CompuCom or hire any person who was or is at any time from the date of execution of the Asset Purchase Agreement to the end of the Non-Competition Period an employee of CompuCom or any Subsidiary of CompuCom.
  > (a) Compu
  > Com agrees that during the Non-Competition Period CompuCom will not, and will not permit any of its
  > Subsidiaries to:
  > (iii) except as contemplated by the Asset Purchase Agreement, solicit, entice or induce any employee of Seller or any Subsidiary of Seller to terminate his or her employment with Seller or any Subsidiary of Seller or hire any person who was or is at any time from the date of execution of the Asset Purchase Agreement to the end of the Non-Competition Period an employee of Seller or any Subsidiary of Seller.
  > Compu
  > Com covenants and agrees that unless otherwise required by law, from and after the Closing:
  > (c) CompuCom shall not solicit or knowingly utilize any of Seller's Confidential Information regarding Seller's Services business from any former employee of Seller.

**Confuser / candidate clauses (first 5 shown in full):**

- `span_id = 84` — (b) CompuCom shall not, directly or indirectly, use, sell, license, publish, disclose or otherwise transfer or make available to others any of Seller's Confidential Information; and
- `span_id = 74` — (b) Seller shall not, directly or indirectly, use, sell, license, publish, disclose, or otherwise transfer or make available to others any of CompuCom's Confidential Information.
- `span_id = 134` — All rights, powers and remedies provided for under this Agreement or otherwise available in respect hereof at law or in equity shall be cumulative and not alternative, and the exercise or beginning of the exercise of any thereof by any party shall not preclude the simultaneous or later exercise of any other such right, power or remedy by such party.
- `span_id = 136` — The failure of any party hereto to exercise any right, power or remedy provided under this Agreement or otherwise available in respect hereof at law or inequity, or to insist upon compliance by any other party hereto with its obligations hereunder, and any custom or practice of the parties at variance with the terms hereof, shall not constitute a waiver by such party of its right to exercise any such or other right, power or remedy or to demand such compliance.
- `span_id = 138` — Each party agrees that, should any court or other competent authority hold any provision of this Agreement or part hereof to be null, void or unenforceable, or order any party to take any action inconsistent herewith or not to take an action consistent herewith or required hereby, the validity, legality and enforceability of the remaining provisions and obligations contained or set forth herein shall not in any way be affected or impaired thereby.


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
391
```

</details>

<details><summary><code>contract_text</code> (truncated)</summary>

```
NON-COMPETITION, REFERRAL AND NON-DISCLOSURE AGREEMENT
NON-COMPETITION, REFERRAL AND NON-DISCLOSURE AGREEMENT (the "Agreement"), dated as of May 10 , 1999, by and between CompuCom Systems, Inc., a Delaware corporation ("CompuCom"), and ENTEX Information Services, Inc., a Delaware corporation ("Seller").
RECITALS
WHEREAS, CompuCom and Seller have entered into an Asset Purchase Agreement dated as of May 10 , 1999 (the "Asset Purchase Agreement");
WHEREAS, the execution of this Agreement is a condition to CompuCom acquiring, and Seller disposing of, the Purchased Assets (as defined in the Asset Purchase Agreement) in connection with the Asset Purchase Agreement;
NOW, THEREFORE, in consideration of the mutual covenants and agreements set forth herein, CompuCom and Seller hereby agree as follows:
1.1 For purposes of this Agreement, the following terms have the following meanings:
(1) "Configuration" means the preparation of a computer and related hardware and integration of components into a computer system; provided that the term "Configuration" shall not include installation of a computer or related hardware at a customer site.
(2) "Non-Competition Period" means the period commencing on May 12, 1999 and ending on May 11, 2000.
(3) "Product" means any computer or related hardware and peripherals (including hubs, switches and routers or networking hardware) or software products (including networking software products) which CompuCom has the ability to sell.
(4) "Product Business"
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

Append your answer to your responses file under the key `"contract:391/hypothesis:nda-18"`. See `responses/EXAMPLE_filled.json`.
