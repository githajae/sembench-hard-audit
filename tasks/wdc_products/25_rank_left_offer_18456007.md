# Audit task — wdc_products / rank

**task_key:** `left_offer:18456007`  
**task_family:** `hard_rank`  
**file stem:** `25_rank_left_offer_18456007`

> Read this page top-to-bottom, then write your two ratings into `responses/<your_name>.json` under the key shown above. See `PROTOCOL.md` for the rubric.

---

## Key facts

*(The inputs the model would see, plus the gold answer with span / sentence ids resolved to their text. These are the facts you actually need to rate Q1 and Q2.)*

**Offer pair under audit:**

- **Left** (id `18456007`, brand `None`, `USD 9.49`)
  > **Title:** RAM® Composite Double Socket Arm
  > **Description:** The RAP-B-201U-A consists of a short double socket arm that accommodates 1" B size ball bases, device holders, and adapters. With an overall length 2.42", this is the lowest profile RAM® double socket arm size. The easy to adjust knob allows for near-infinite adjustability for your connected device.

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
  94106554,
  53451198,
  12959047,
  71290070,
  53660770,
  75462645,
  30675144
]
```

</details>

<details><summary><code>candidate_order_seed</code></summary>

```
18456007
```

</details>

<details><summary><code>candidate_right_offers</code></summary>

```
[
  {
    "id": 94106554,
    "brand": "RAM Mounts",
    "title": "RAM Mounts short arm for 1\\\" ball",
    "description": "The RAP-B-201U-A, short double socket arm, has a socket at both ends that accommodates 1\\\" ball bases. This socket technology allows for almost infinite adjustment and perfect viewing angles.(This product does not include single spring)Dimensions:Overall Length: 2.42\\\"Socket-To-Socket Length:",
    "price": "9.63",
    "price_currency": "eur",
    "cluster_id": 3656260,
    "pair_id": "18456007#94106554",
    "is_hard_negative": false,
    "gold_label": "match"
  },
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
4
```

</details>

<details><summary><code>hard_same_brand_confuser_count</code></summary>

```
4
```

</details>


---

## Audit questions

**Q1 — Naturalness (1–5).** Does this hardened task still look like a natural operator problem? See `PROTOCOL.md`.

**Q2 — Verifier validity.** Would the verifier rule above accept the same outputs you would accept on this task? Choose `agree`, `disagree_too_strict`, `disagree_too_lax`, or `disagree_other`.

Append your answer to your responses file under the key `"left_offer:18456007"`. See `responses/EXAMPLE_filled.json`.
