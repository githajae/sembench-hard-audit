# Audit task — wdc_products / rank

**task_key:** `left_offer:86176880`  
**task_family:** `hard_rank`  
**file stem:** `30_rank_left_offer_86176880`

> Read this page top-to-bottom, then write your two ratings into `responses/<your_name>.json` under the key shown above. See `PROTOCOL.md` for the rubric.

---

## Key facts

*(The inputs the model would see, plus the gold answer with span / sentence ids resolved to their text. These are the facts you actually need to rate Q1 and Q2.)*

**Offer pair under audit:**

- **Left** (id `86176880`, brand `None`, `CAD 1099.99`)
  > **Title:** Sigma ART 50mm f/1.4 DG HSM Lens for Nikon

**Gold decisive attributes:** `['title']`
**`top_k` (rank length):** `3`


---

## Verifier rule (what the strict verifier checks)

> Output is a ranked list of right-side offer ids of length `top_k`. Accept iff the top-`k` set contains the gold matching offer (and gold non-matches are not above it).

This rule is the contract you are auditing in **Q2**.

---

## Policy / instructions (as the model sees them)

> Choose the single best same-product candidate for the reference offer. Treat same-brand accessories, bundles, neighboring model numbers, and storage or color variants as confusers rather than true matches. Use only the minimal decisive attributes.

---

## Other fields (collapsed, for reference)

<details><summary><code>candidate_ids</code></summary>

```
[
  26301462,
  32931015,
  26736430,
  31585097,
  78989521
]
```

</details>

<details><summary><code>candidate_order_seed</code></summary>

```
86176880
```

</details>

<details><summary><code>candidate_right_offers</code></summary>

```
[
  {
    "id": 26301462,
    "brand": "Sigma",
    "title": "Sigma 35mm F1.4 DG Art HSM EOS Mount Lens",
    "description": "Sigma 35mm F1.4 DG Art HSM EOS Mount Lens",
    "price": "1059",
    "price_currency": "AUD",
    "cluster_id": 704991,
    "pair_id": "97657130#26301462",
    "is_hard_negative": true,
    "gold_label": "non_match"
  },
  {
    "id": 32931015,
    "brand": null,
    "title": "Sigma 105mm f1.4 DG HSM Art Lens for Canon",
    "description": "105mm Filter Size f/1.4 Aperture N/A Stabilized EF Mount The “Bokeh Master” Optical system delivering unsurpassed f/1.4 performance
... [truncated, full content in the .json file] ...
```

</details>

<details><summary><code>hard_candidate_count</code></summary>

```
5
```

</details>

<details><summary><code>hard_max_confuser_overlap</code></summary>

```
8
```

</details>

<details><summary><code>hard_same_brand_confuser_count</code></summary>

```
2
```

</details>


---

## Audit questions

**Q1 — Naturalness (1–5).** Does this hardened task still look like a natural operator problem? See `PROTOCOL.md`.

**Q2 — Verifier validity.** Would the verifier rule above accept the same outputs you would accept on this task? Choose `agree`, `disagree_too_strict`, `disagree_too_lax`, or `disagree_other`.

Append your answer to your responses file under the key `"left_offer:86176880"`. See `responses/EXAMPLE_filled.json`.
