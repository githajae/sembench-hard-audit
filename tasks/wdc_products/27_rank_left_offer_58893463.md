# Audit task — wdc_products / rank

**task_key:** `left_offer:58893463`  
**task_family:** `hard_rank`  
**file stem:** `27_rank_left_offer_58893463`

> Read this page top-to-bottom, then write your two ratings into `responses/<your_name>.json` under the key shown above. See `PROTOCOL.md` for the rubric.

---

## Key facts

*(The inputs the model would see, plus the gold answer with span / sentence ids resolved to their text. These are the facts you actually need to rate Q1 and Q2.)*

**Offer pair under audit:**

- **Left** (id `58893463`, brand `None`, `USD 44.95`)
  > **Title:** 32 Oz Wide Mouth With Flex Cap W32BTS001
  > **Description:** 32 Oz Wide Mouth With Flex Cap W32BTS001Product DescriptionBrand : Hydro FlaskStyle# : W32BTS001Product Type : Water BottleColor : BlackVolume : 32 oz

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
  9069903,
  11665937,
  12190772,
  50789754,
  41191422,
  41456801
]
```

</details>

<details><summary><code>candidate_order_seed</code></summary>

```
58893463
```

</details>

<details><summary><code>candidate_right_offers</code></summary>

```
[
  {
    "id": 9069903,
    "brand": null,
    "title": "21 oz Standard Mouth With Standard S21SX306",
    "description": "Product DescriptionBrand : HYDRO FLASKStyle# : S21SX306Product Type : TumblerColor : OLIVESize : 21oz(621mL)Material :18/8 Pro Grade Stainless SteelOrigin : ImportedFeaturesVersatile, middle-of-the-road sizeTempShield??insulation eliminates condensation and keeps beverages cold up to 24 hours and hot up to 12 hoursDurable 18/8 Pro-Grade Stainless Steel constructionBPA-Free and Phthalate-FreeCompatible with Standard Mouth Insulated Sport CapLifetime Warranty",
    "price":
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
6
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

Append your answer to your responses file under the key `"left_offer:58893463"`. See `responses/EXAMPLE_filled.json`.
