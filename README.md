# SemBench-Hard Human/Expert Calibration Kit

A small audit kit that asks two questions about every hardened
task in [SemBench-Hard](https://github.com/) (Appendix D):

1. **Task naturalness** — does the hardened task still look like a
   natural operator problem? (5-point Likert)
2. **Verifier validity** — would the strict verifier accept the
   same outputs an informed human would accept? (binary)

You hand this folder to an annotator (or to your favourite LLM with
a human in the loop). They produce one JSON file. The aggregator
turns it into a paper-style summary table.

---

## One-click — pick your path

### A. With Claude Code / Cowork (recommended)

You don't need to read the rest of this. Open this folder with
Claude Code (or any client that respects `CLAUDE.md`) and say:

> **"Let's run the audit."**

Claude reads `CLAUDE.md` and walks you through every task — picks
the next un-rated one, summarizes it, gives its own tentative
rating with reasoning, asks you to confirm, saves the response,
and loops. You can stop any time and resume by saying
**"continue audit"**.

### B. Plain terminal (no LLM helper)

```bash
git clone https://github.com/githajae/sembench-hard-audit.git
cd sembench-hard-audit
python scripts/annotate.py --user <your_id>
```

That CLI walks you through tasks one at a time, prompting for
naturalness (1–5) and verifier validity (`agree` /
`disagree_too_strict` / `disagree_too_lax` / `disagree_other`)
and saving to `responses/<your_id>.json`.

If you want an LLM as a co-pilot in this mode:

```bash
python scripts/annotate.py --user <your_id> --show-llm-prompt
```

It prints the LLM_PROMPT.md template with the current task's JSON
inlined; paste it into Claude/ChatGPT/Gemini, read its rationale,
and then answer the CLI yourself.

### C. Fully manual (you write the JSON)

1. Open task pages in `tasks/<benchmark>/NN_<operator>_*.md`.
2. Copy `responses/template.json` to `responses/<your_id>.json`.
3. For each task, append an entry under the manifest's `task_key`
   (verbatim) with `naturalness`, `verifier_validity`,
   `confidence`, and (optional) `notes`.

---

## When everyone is done

```bash
python scripts/aggregate.py
```

Writes:

- `results/summary.json` and `results/summary.md` — paper Table 18
  layout (naturalness ≥4 %, verifier agree %, Cohen's κ across
  annotator pairs, retained disagreements).
- `results/disagreements.md` — every retained disagreement with
  notes, suitable for the qualitative appendix.
- `results/per_annotator.csv` — per-annotator headline rates.

Add `--high-confidence-only` to drop ratings that the annotator
flagged as `confidence: "low"`.

---

## Reading order

| If you have | Read |
| --- | --- |
| 5 minutes | this `README.md` |
| 10 minutes (recommended) | `PROTOCOL.md` (rubric, decision rule) |
| 30 minutes (annotator pre-flight) | `INTRODUCTION.md` → `PROTOCOL.md` → `ANNOTATOR_GUIDE.md` |
| using Cowork | nothing else; Claude reads `CLAUDE.md` for you |

---

## Folder layout

```
.
├── README.md                 # this file
├── CLAUDE.md                 # Cowork / Claude Code driver
├── INTRODUCTION.md           # paper context, why audit
├── PROTOCOL.md               # the two questions, rubric, examples
├── ANNOTATOR_GUIDE.md        # human-only run instructions
├── LLM_PROMPT.md             # LLM co-pilot prompt template
├── scripts/
│   ├── annotate.py           # interactive CLI ← path B
│   ├── build_tasks.py        # rebuild tasks/ from SemBench-Hard data
│   ├── render_tasks.py       # rebuild tasks/*.md from tasks/*.json
│   ├── aggregate.py          # responses → results
│   ├── requirements.txt
│   └── README.md
├── tasks/
│   ├── manifest.json         # 120 task index (when fully populated)
│   ├── contractnli/          # 30 tasks × .json + .md (pre-shipped)
│   ├── wdc_products/         # 30 tasks × .json + .md (pre-shipped)
│   ├── scifact/              # populate via build_tasks.py
│   └── swebench_verified/    # populate via build_tasks.py
├── responses/
│   ├── template.json         # blank template
│   └── EXAMPLE_filled.json   # filled example (aggregator skips it)
└── results/                  # aggregator output
```

The kit ships with **60 tasks pre-generated** (`contractnli` +
`wdc_products`). To fill in `scifact` and `swebench_verified`, the
SemBench-Hard maintainer runs `python scripts/build_tasks.py` from
inside their main repo (where `code/benchmarks/` is available) and
copies the output `tasks/` into this kit before distributing.
