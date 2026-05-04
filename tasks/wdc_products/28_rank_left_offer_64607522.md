# Audit task — wdc_products / rank

**task_key:** `left_offer:64607522`  
**task_family:** `hard_rank`  
**file stem:** `28_rank_left_offer_64607522`

> Read this page top-to-bottom, then write your two ratings into `responses/<your_name>.json` under the key shown above. See `PROTOCOL.md` for the rubric.

---

## Key facts

*(The inputs the model would see, plus the gold answer with span / sentence ids resolved to their text. These are the facts you actually need to rate Q1 and Q2.)*

**Offer pair under audit:**

- **Left** (id `64607522`, brand `Manfrotto`, `GBP 115`)
  > **Title:** Manfrotto MVH500AH Lightweight Video Head with Flat Base
  > **Description:** The Manfrotto MVH500AH is a lightweight head with a wider platform for HDSLR bodies which has a sliding plate which travels to balance the latest interchangeable lens cameras.

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
  37865200,
  62242632,
  48435137,
  35405134,
  91625850,
  8174351,
  22563019
]
```

</details>

<details><summary><code>candidate_order_seed</code></summary>

```
64607522
```

</details>

<details><summary><code>candidate_right_offers</code></summary>

```
[
  {
    "id": 37865200,
    "brand": null,
    "title": "Manfrotto MVK500AM Fluid Video Head With Lightweight Telescopic Legs",
    "description": "The lightweight fluid video system MVK500AM includes the fluid video head (60mm half ball) MVH500A and the twin leg video tripod MVT502AM.",
    "price": "369.00",
    "price_currency": "GBP",
    "cluster_id": 645102,
    "pair_id": "79558814#37865200",
    "is_hard_negative": false,
    "gold_label": "match"
  },
  {
    "id": 62242632,
    "brand": "Epson",
    "title": "Epson Blekk Svart T7031 L - WP4000/4500",
    "description": null,
    "p
... [truncated, full content in the .json file] ...
```

</details>

<details><summary><code>hard_candidate_count</code></summary>

```
7
```

</details>

<details><summary><code>hard_max_confuser_overlap</code></summary>

```
5
```

</details>

<details><summary><code>hard_same_brand_confuser_count</code></summary>

```
1
```

</details>


---

## Audit questions

**Q1 — Naturalness (1–5).** Does this hardened task still look like a natural operator problem? See `PROTOCOL.md`.

**Q2 — Verifier validity.** Would the verifier rule above accept the same outputs you would accept on this task? Choose `agree`, `disagree_too_strict`, `disagree_too_lax`, or `disagree_other`.

Append your answer to your responses file under the key `"left_offer:64607522"`. See `responses/EXAMPLE_filled.json`.
