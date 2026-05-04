# scripts/

Three small CLIs. None of them mutate the repo outside `human_audit/`.

| Script | What it does |
| --- | --- |
| `build_tasks.py` | Sample 30 hard tasks per benchmark (4 × 30 = 120) using the loaders in `code/benchmarks/section_5_1.py`. Writes `tasks/manifest.json` and one `.json` per task. Deterministic given `--seed`. |
| `render_tasks.py` | For every entry in `tasks/manifest.json`, write a sibling `.md` file containing a human-readable view of the task plus a verifier-rule summary. |
| `aggregate.py` | Read every `responses/<annotator>.json`, compute pooled and per-annotator stats, write `results/summary.{json,md}`, `results/disagreements.md`, and `results/per_annotator.csv`. |

## Order of operations

```
build_tasks.py     →   tasks/manifest.json + tasks/*/*.json
render_tasks.py    →   tasks/*/*.md
(annotators fill responses/*.json)
aggregate.py       →   results/*
```

## Tip

If `build_tasks.py` fails with an ImportError or a missing-data
RuntimeError, look at the message — the loaders explain how to set
up each dataset (e.g. the SciFact body-augmented subset must be
prepared with `python code/scripts/setup_data.py --datasets scifact`
first).
