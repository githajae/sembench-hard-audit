# Audit task — wdc_products / rank

**task_key:** `left_offer:27347346`  
**task_family:** `hard_rank`  
**file stem:** `29_rank_left_offer_27347346`

> Read this page top-to-bottom, then write your two ratings into `responses/<your_name>.json` under the key shown above. See `PROTOCOL.md` for the rubric.

---

## Key facts

*(The inputs the model would see, plus the gold answer with span / sentence ids resolved to their text. These are the facts you actually need to rate Q1 and Q2.)*

**Offer pair under audit:**

- **Left** (id `27347346`, brand `None`, `None None`)
  > **Title:** SEAGATE SATA-3 2TB SSHD FIRECUDA

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
  83418921,
  84438504,
  81351830,
  27923177,
  90183159,
  6020197
]
```

</details>

<details><summary><code>candidate_order_seed</code></summary>

```
27347346
```

</details>

<details><summary><code>candidate_right_offers</code></summary>

```
[
  {
    "id": 83418921,
    "brand": null,
    "title": "8TB - Seagate Enterprise Ironwolf Pro SATA - ST8000NE001",
    "description": "[shortdesc]Seagate IronWolf Pro ST8000NE001 8TB 7200RPM 256MB Cache SATA 6.0Gb/s 3.5\\\" Internal Hard Drive.7200 RPM 256MB CacheSATA 6.0Gb/sEnterprise NAS Hard Drives[/shortdesc][additional]Manufacturer :SynologyBrand :SeagateProduct Line :Seagate IronWolf ProModel :ST8000NE001Bundled with :2 years Rescue Data Recovery Service PlanPackaged Quantity :1StorageType :Hard driveHard DriveHard Drive Type :Internal hard driveForm Factor :3.5\\\"Form Factor (metric
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

Append your answer to your responses file under the key `"left_offer:27347346"`. See `responses/EXAMPLE_filled.json`.
