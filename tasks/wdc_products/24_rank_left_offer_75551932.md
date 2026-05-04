# Audit task — wdc_products / rank

**task_key:** `left_offer:75551932`  
**task_family:** `hard_rank`  
**file stem:** `24_rank_left_offer_75551932`

> Read this page top-to-bottom, then write your two ratings into `responses/<your_name>.json` under the key shown above. See `PROTOCOL.md` for the rubric.

---

## Key facts

*(The inputs the model would see, plus the gold answer with span / sentence ids resolved to their text. These are the facts you actually need to rate Q1 and Q2.)*

**Offer pair under audit:**

- **Left** (id `75551932`, brand `None`, `AUD 5.0E1`)
  > **Title:** Hydro Flask 21 Oz- Black
  > **Description:** Hydroflask 21oz bottle is the perfect companion for the beach, trail or everyday use.Versatile, middle-of-the-road sizeTempShield™ insulation eliminates condensation and keeps beverages cold up to 24 hours and hot up to 12 hoursDurable 18/8 Pro-Grade Stainless Steel constructionBPA-Free and Phthalate-FreeCompatible with standard mouth insulated sport cap

**Gold decisive attributes:** `['price', 'title']`
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
  12190772,
  12243414,
  60571140,
  11665937,
  50789754,
  2687477
]
```

</details>

<details><summary><code>candidate_order_seed</code></summary>

```
75551932
```

</details>

<details><summary><code>candidate_right_offers</code></summary>

```
[
  {
    "id": 12190772,
    "brand": "HYDRO FLASK",
    "title": "HYDRO FLASK HYDRO FLASK 32OZ WIDE MOUTH BOTTLE-BLACK",
    "description": "Big enough for a whole day on the river or trails, the Hydro Flask 32 oz Wide Mouth Bottle is made with professional-grade stainless steel and a wider opening for faster fill. The Color Last™ powder coat is dishwasher safe for even more convenience. Cold",
    "price": "44.95",
    "price_currency": "USD",
    "cluster_id": 36023,
    "pair_id": "75551932#12190772",
    "is_hard_negative": true,
    "gold_label": "non_match"
  },
  {
    "id": 12243414,
... [truncated, full content in the .json file] ...
```

</details>

<details><summary><code>hard_candidate_count</code></summary>

```
6
```

</details>

<details><summary><code>hard_max_confuser_overlap</code></summary>

```
4
```

</details>

<details><summary><code>hard_same_brand_confuser_count</code></summary>

```
0
```

</details>


---

## Audit questions

**Q1 — Naturalness (1–5).** Does this hardened task still look like a natural operator problem? See `PROTOCOL.md`.

**Q2 — Verifier validity.** Would the verifier rule above accept the same outputs you would accept on this task? Choose `agree`, `disagree_too_strict`, `disagree_too_lax`, or `disagree_other`.

Append your answer to your responses file under the key `"left_offer:75551932"`. See `responses/EXAMPLE_filled.json`.
