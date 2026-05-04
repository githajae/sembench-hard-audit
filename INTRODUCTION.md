# Introduction — Why We Run This Audit

> Read time: ~5 minutes.

## 1. What is SemBench-Hard?

SemBench-Hard is a benchmark for **declarative semantic operators** —
the `Map`, `Filter`, `Join`, and `Rank` operators that recent LLM-based
data systems (Palimpzest, DocETL, ThalamusDB, …) expose to users.

For each of four source datasets, the benchmark provides paired
versions of every operator call:

| Benchmark | Domain | Task unit |
| --- | --- | --- |
| **SWE-bench Verified** | Software engineering | Issue + candidate patches |
| **SciFact** | Scientific claim verification | Claim + paper |
| **ContractNLI** | Legal NDAs | Contract + hypothesis |
| **WDC Products** | E-commerce entity matching | Pair of product offers |

Each (benchmark × operator) cell has two modes:

- **base** — the canonical, mildly-formatted operator call.
- **hard** — the same source instance, hardened along four axes
  (context, constraint, schema, verification) so that shallow
  pattern-matching no longer suffices.

The paper claims that hardening produces a large, distributionally
strict drop in operator accuracy across systems and models.

## 2. The risk this audit addresses

A skeptical reader can object as follows:

> "What if hardening just makes the tasks *awkwardly worded* rather
> than genuinely harder? Maybe the strict verifiers reject outputs
> that a competent human would accept."

If that were true, the headline drop (paper Section 5) would be a
formatting artifact, not evidence about model reasoning.

The Human and Expert Calibration audit (paper Appendix D) is designed
to falsify that worry directly:

- **Q1: Task naturalness.** Does the hardened task still look like a
  reasonable operator problem to a domain-aware reader?
- **Q2: Verifier validity.** When the annotator decides the model's
  output is correct, would the strict verifier also accept it? When
  the annotator says it is wrong, does the verifier reject it?

If both rates are high (and the paper reports 87% / 92% with
κ = 0.78), then the hardened drop is not explained away by awkward
formulation or over-strict verifiers.

## 3. Why a small audit is enough

The audit is **not** a re-annotation of the benchmark. It is a
calibration: a small but carefully sampled slice that lets the reader
trust the rest of the numbers.

- **N = 120 tasks** (30 per benchmark, stratified across the 4
  operators) is enough for a tight Cohen's κ estimate at the
  verifier-validity cell level, and sufficient to make a binomial
  confidence statement about naturalness ≥ some target.
- Each task is reviewed independently by **two domain-aware
  annotators**, so disagreements are captured rather than hidden.
- Ambiguous cases are not silently resolved — they are written to
  `results/disagreements.md` and discussed qualitatively in the
  paper's prose.

## 4. What this kit gives you

- A deterministic, seeded sample so any two annotators audit the
  *same* 120 tasks (matches the paper's `seed = 20260504`).
- Each task rendered both as a JSON object (for LLMs) and as a
  Markdown page (for humans), with the policy text, the gold
  answer, and the verifier's accept rule visible.
- A clean response template plus an aggregation script that prints
  the same statistics the paper reports.

## 5. Threats to validity (please read)

Even with this kit, please remember:

- **Annotator expertise matters.** SWE-bench Verified asks about real
  Python patches and tests; SciFact asks about biomedical claims;
  ContractNLI about legal NDA clauses; WDC about product attributes.
  An annotator who blindly defers to an LLM on an unfamiliar domain
  *adds noise* rather than signal. If you are not comfortable with
  a domain, mark `confidence: low` on that task — the aggregator can
  optionally exclude low-confidence ratings from the headline number.
- **The audit measures verifier–annotator agreement, not
  ground-truth correctness.** A high agreement number says the
  verifier is consistent with informed humans. It does not by itself
  prove the gold label is correct in every case.
- **Hardening is not "make it impossible".** A natural hardened task
  should still be solvable in principle by a careful expert with the
  full evidence. If a task is unsolvable even in principle, mark it
  `naturalness ≤ 2` and note why in `notes`.

Now read `PROTOCOL.md` for the exact rubric.
