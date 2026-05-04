# Audit task — contractnli / join

**task_key:** `contract:504/hypothesis:nda-1/span:22`  
**task_family:** `hard_join`  
**file stem:** `16_join_contract_504_hypothesis_nda-1_span_22`

> Read this page top-to-bottom, then write your two ratings into `responses/<your_name>.json` under the key shown above. See `PROTOCOL.md` for the rubric.

---

## Key facts

*(The inputs the model would see, plus the gold answer with span / sentence ids resolved to their text. These are the facts you actually need to rate Q1 and Q2.)*

**Hypothesis** (the claim about the contract):

> All Confidential Information shall be expressly identified by the Disclosing Party.

**Candidate clause** (`span_id = 22`):

> (w) such information may be disclosed by EnCana to its Representatives who need to know such information for the purpose of evaluating the Transaction or their participation therein (it being understood that such Representatives shall be informed of the confidential nature of the information),

**Gold label:** `not_evidence`

**Confuser / candidate clauses (first 5 shown in full):**

- `span_id = 41` — In the event of such a decision or request, all other Evaluation Material prepared by EnCana shall be destroyed, and in no event shall EnCana be obligated to disclose or provide the Evaluation Material prepared by it or its Representatives to TBI provided that a single copy of each item returned or destroyed may be retained in the files of EnCana's outside legal counsel for the purpose of resolving any disputes that may arise under this letter agreement.
- `span_id = 37` — If, in the absence of a protective order or other remedy, or the receipt of a waiver by TBI, EnCana or any of its Representatives should nonetheless, based on the advice of such party's counsel, disclose the Evaluation Material and/or the facts or information covered by Section 2, EnCana or its Representative may, without liability hereunder, disclose only that portion of the Evaluation Material and/or such facts or information that such counsel advises is legally required to be disclosed; provided that EnCana gives TBI written notice of the Evaluation Material and/or such facts or other infor
- `span_id = 21` — Accordingly, EnCana agrees that the Evaluation Material will be used solely for the purpose of evaluating the Transaction and related actions, and that such information will be kept confidential by EnCana and its Representatives; provided, however, that
- `span_id = 70` — Representatives who are informed as to the matters that arc the subject of this agreement, that the United States securities laws may prohibit any person who has material, nonpublic information concerning the matters that are the subject of this agreement from purchasing or selling securities of a company that may be a party to a transaction of the type contemplated by this agreement or from communicating such information to any other person under circumstances in which it is reasonably foreseeable that such person is likely to purchase or sell such securities.
- `span_id = 24` — (y) it shall not constitute a breach of this letter agreement for EnCana or its Representatives to disclose such information to the extent that EnCana believes, based on the advice of counsel, that it is legally required to disclose such information in order to avoid committing a violation of any law, rule or regulation, including any rules or regulations of any securities association, stock exchange or national securities quotation system, provided that EnCana provides prompt notice to TBI of the proposed disclosure and takes the other actions required in connection with a required disclosure


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
504
```

</details>

<details><summary><code>span_text</code></summary>

```
(w) such information may be disclosed by EnCana to its Representatives who need to know such information for the purpose of evaluating the Transaction or their participation therein (it being understood that such Representatives shall be informed of the confidential nature of the information), 
```

</details>


---

## Audit questions

**Q1 — Naturalness (1–5).** Does this hardened task still look like a natural operator problem? See `PROTOCOL.md`.

**Q2 — Verifier validity.** Would the verifier rule above accept the same outputs you would accept on this task? Choose `agree`, `disagree_too_strict`, `disagree_too_lax`, or `disagree_other`.

Append your answer to your responses file under the key `"contract:504/hypothesis:nda-1/span:22"`. See `responses/EXAMPLE_filled.json`.
