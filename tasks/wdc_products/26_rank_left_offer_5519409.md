# Audit task — wdc_products / rank

**task_key:** `left_offer:5519409`  
**task_family:** `hard_rank`  
**file stem:** `26_rank_left_offer_5519409`

> Read this page top-to-bottom, then write your two ratings into `responses/<your_name>.json` under the key shown above. See `PROTOCOL.md` for the rubric.

---

## Key facts

*(The inputs the model would see, plus the gold answer with span / sentence ids resolved to their text. These are the facts you actually need to rate Q1 and Q2.)*

**Offer pair under audit:**

- **Left** (id `5519409`, brand `None`, `USD 18.99`)
  > **Title:** Evans 14\" TT14EC2S Clear Drum Head
  > **Description:** Evans EC2 Clear series contains two plies of 7mil film for optimized attack, tone, length of sustain, and ease of tuning for each size head. This drumhead features Sound Shaping Technology (SST) for a well-balanced sound, incorporated with Evans Level 360 Technology for ease of tuning, extended pitch range and optimum quality of sound.IDEAL FOR:ROCKGOSPELPOP

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
  47293324,
  21963707,
  52799959,
  16154426,
  9232364,
  1136383
]
```

</details>

<details><summary><code>candidate_order_seed</code></summary>

```
5519409
```

</details>

<details><summary><code>candidate_right_offers</code></summary>

```
[
  {
    "id": 47293324,
    "brand": "Evans",
    "title": "Evans EC2 Clear Drum Head, 8 Inch",
    "description": "Evans clear EC2 series features two plies of 7mil film with optimized attack, tone, length of sustain and ease of tuning for each size head. The Sound Shaping Technology (SST) Edge Control ring mounted on the underside delivers an extremely well balanced and pre-EQ'd sound across the full kit by varying the size of the ring for each different head size.Evans Level 360 technology is incorporated to extend the level playing surface of the drumhead, 360 degrees around the drum. Th
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
0
```

</details>


---

## Audit questions

**Q1 — Naturalness (1–5).** Does this hardened task still look like a natural operator problem? See `PROTOCOL.md`.

**Q2 — Verifier validity.** Would the verifier rule above accept the same outputs you would accept on this task? Choose `agree`, `disagree_too_strict`, `disagree_too_lax`, or `disagree_other`.

Append your answer to your responses file under the key `"left_offer:5519409"`. See `responses/EXAMPLE_filled.json`.
