#!/usr/bin/env python3
"""Aggregate annotator response files into the calibration summary.

Reads every `responses/*.json` (excluding `template.json` and any file
starting with `EXAMPLE`), validates the shape, then produces:

    results/summary.json    # machine-readable summary
    results/summary.md      # paper-style markdown table (Table 18)
    results/disagreements.md
    results/per_annotator.csv

Usage:

    python scripts/aggregate.py
    python scripts/aggregate.py --responses-dir /path/to/responses
    python scripts/aggregate.py --high-confidence-only

Numbers reproduced (target, paper Table 18):

    - Task naturalness:       % rated >= 4 on 5-point Likert.
    - Verifier validity:      % answered "agree".
    - Cohen's kappa:          annotator-vs-verifier agreement
                              (treats verifier as a constant "agree" rater
                              by construction; kappa is computed across
                              the two annotators on the binary
                              agree/disagree judgement, then reported as
                              the audit's reliability number).
    - Retained disagreements: tasks where any annotator answered
                              `disagree_*`.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

HERE = Path(__file__).resolve()
KIT_ROOT = HERE.parent.parent
DEFAULT_RESPONSES = KIT_ROOT / "responses"
DEFAULT_TASKS = KIT_ROOT / "tasks"
DEFAULT_RESULTS = KIT_ROOT / "results"

VALID_VERIFIER_VALUES = {
    "agree",
    "disagree_too_strict",
    "disagree_too_lax",
    "disagree_other",
}
VALID_CONFIDENCE = {"high", "medium", "low"}


def _percent(num: int, denom: int) -> float:
    return 100.0 * num / denom if denom else float("nan")


def cohen_kappa(rater_a: List[str], rater_b: List[str]) -> float:
    """Cohen's kappa for two raters over the same items.

    Inputs must be lists of equal length with discrete labels.
    Returns NaN if denominator is zero.
    """
    if len(rater_a) != len(rater_b):
        raise ValueError("raters must label the same items")
    n = len(rater_a)
    if n == 0:
        return float("nan")
    labels = sorted(set(rater_a) | set(rater_b))
    if len(labels) < 2:
        # Perfect agreement on a single label -> kappa undefined (0/0).
        # Convention: return 1.0 if all match, NaN if mismatched lengths.
        return 1.0 if rater_a == rater_b else float("nan")
    obs = sum(1 for a, b in zip(rater_a, rater_b) if a == b) / n
    pa = Counter(rater_a)
    pb = Counter(rater_b)
    expected = sum((pa[l] / n) * (pb[l] / n) for l in labels)
    if math.isclose(expected, 1.0):
        return float("nan")
    return (obs - expected) / (1 - expected)


def load_response_file(path: Path) -> Dict[str, Any]:
    with path.open(encoding="utf-8") as fh:
        data = json.load(fh)
    if "annotator_id" not in data or "ratings" not in data:
        raise ValueError(
            f"{path.name}: response file must contain 'annotator_id' and 'ratings'"
        )
    if not isinstance(data["ratings"], dict):
        raise ValueError(f"{path.name}: 'ratings' must be a dict keyed by task_key")
    return data


def validate_rating(task_key: str, rating: Dict[str, Any], annotator: str) -> None:
    nat = rating.get("naturalness")
    if not isinstance(nat, int) or not (1 <= nat <= 5):
        raise ValueError(
            f"{annotator} / {task_key}: naturalness must be int in [1,5], got {nat!r}"
        )
    val = rating.get("verifier_validity")
    if val not in VALID_VERIFIER_VALUES:
        raise ValueError(
            f"{annotator} / {task_key}: verifier_validity must be one of "
            f"{sorted(VALID_VERIFIER_VALUES)}, got {val!r}"
        )
    conf = rating.get("confidence")
    if conf is not None and conf not in VALID_CONFIDENCE:
        raise ValueError(
            f"{annotator} / {task_key}: confidence must be in "
            f"{sorted(VALID_CONFIDENCE)} or omitted, got {conf!r}"
        )
    if val != "agree" and not str(rating.get("notes", "")).strip():
        sys.stderr.write(
            f"[aggregate] warning: {annotator} / {task_key}: "
            f"verifier_validity={val} but notes are empty.\n"
        )


def load_manifest(tasks_dir: Path) -> Optional[Dict[str, Any]]:
    p = tasks_dir / "manifest.json"
    if not p.exists():
        return None
    with p.open(encoding="utf-8") as fh:
        return json.load(fh)


def collect_responses(responses_dir: Path) -> List[Dict[str, Any]]:
    files = []
    for p in sorted(responses_dir.glob("*.json")):
        if p.name == "template.json" or p.name.startswith("EXAMPLE"):
            continue
        files.append(load_response_file(p))
    if not files:
        raise RuntimeError(
            f"no annotator response files found under {responses_dir} "
            "(template.json and EXAMPLE*.json are skipped). "
            "Each annotator should write to responses/<their_name>.json."
        )
    return files


def aggregate(
    responses: List[Dict[str, Any]],
    manifest: Optional[Dict[str, Any]],
    high_confidence_only: bool,
) -> Dict[str, Any]:
    # task_key -> entry meta (benchmark, operator) for breakdowns
    meta_by_key: Dict[str, Dict[str, str]] = {}
    if manifest:
        for entry in manifest["entries"]:
            meta_by_key[entry["task_key"]] = {
                "benchmark": entry["benchmark"],
                "operator": entry["operator"],
            }

    # Validate every rating up front.
    known_keys = set(meta_by_key.keys()) if meta_by_key else None
    for resp in responses:
        for task_key, rating in resp["ratings"].items():
            validate_rating(task_key, rating, resp["annotator_id"])
            if known_keys is not None and task_key not in known_keys:
                sys.stderr.write(
                    f"[aggregate] warning: {resp['annotator_id']} rated "
                    f"task_key {task_key!r}, which is not in the manifest. "
                    "It will be aggregated under benchmark/operator '?/?'. "
                    "Check for a typo in the response file.\n"
                )

    # --- per-annotator headline ------------------------------------------------
    per_annot: List[Dict[str, Any]] = []
    for resp in responses:
        ratings = resp["ratings"]
        if high_confidence_only:
            ratings = {
                k: v for k, v in ratings.items()
                if v.get("confidence", "high") != "low"
            }
        n = len(ratings)
        if n == 0:
            per_annot.append({
                "annotator_id": resp["annotator_id"],
                "n": 0,
                "naturalness_ge4_pct": float("nan"),
                "verifier_agree_pct": float("nan"),
            })
            continue
        n_natural = sum(1 for v in ratings.values() if v["naturalness"] >= 4)
        n_agree = sum(1 for v in ratings.values()
                      if v["verifier_validity"] == "agree")
        per_annot.append({
            "annotator_id": resp["annotator_id"],
            "n": n,
            "naturalness_ge4_pct": _percent(n_natural, n),
            "verifier_agree_pct": _percent(n_agree, n),
        })

    # --- pooled headline -------------------------------------------------------
    pooled_naturalness: List[int] = []
    pooled_validity: List[str] = []
    for resp in responses:
        for v in resp["ratings"].values():
            if high_confidence_only and v.get("confidence", "high") == "low":
                continue
            pooled_naturalness.append(int(v["naturalness"]))
            pooled_validity.append(v["verifier_validity"])
    n_pool = len(pooled_naturalness)
    n_natural = sum(1 for x in pooled_naturalness if x >= 4)
    n_agree = sum(1 for x in pooled_validity if x == "agree")
    pooled = {
        "n": n_pool,
        "naturalness_ge4_pct": _percent(n_natural, n_pool),
        "verifier_agree_pct": _percent(n_agree, n_pool),
        "verifier_label_counts": dict(Counter(pooled_validity)),
        "naturalness_distribution": dict(sorted(Counter(pooled_naturalness).items())),
    }

    # --- per-benchmark / per-operator breakdown -------------------------------
    per_cell: Dict[Tuple[str, str], Dict[str, int]] = defaultdict(
        lambda: {"n": 0, "ge4": 0, "agree": 0}
    )
    for resp in responses:
        for task_key, v in resp["ratings"].items():
            if high_confidence_only and v.get("confidence", "high") == "low":
                continue
            meta = meta_by_key.get(task_key, {"benchmark": "?", "operator": "?"})
            cell = (meta["benchmark"], meta["operator"])
            per_cell[cell]["n"] += 1
            if v["naturalness"] >= 4:
                per_cell[cell]["ge4"] += 1
            if v["verifier_validity"] == "agree":
                per_cell[cell]["agree"] += 1

    cell_summary = {
        f"{b}/{o}": {
            "n": d["n"],
            "naturalness_ge4_pct": _percent(d["ge4"], d["n"]),
            "verifier_agree_pct": _percent(d["agree"], d["n"]),
        }
        for (b, o), d in sorted(per_cell.items())
    }

    # --- Cohen's kappa across annotator pairs ---------------------------------
    # We compute kappa on the binary (agree vs not) verifier-validity judgement
    # for every pair of annotators, restricted to tasks both annotators rated.
    pair_kappas: List[Dict[str, Any]] = []
    n_annot = len(responses)
    for i in range(n_annot):
        for j in range(i + 1, n_annot):
            a, b = responses[i], responses[j]
            common = set(a["ratings"]) & set(b["ratings"])
            if high_confidence_only:
                common = {
                    k for k in common
                    if a["ratings"][k].get("confidence", "high") != "low"
                    and b["ratings"][k].get("confidence", "high") != "low"
                }
            if not common:
                continue
            la = ["agree" if a["ratings"][k]["verifier_validity"] == "agree"
                  else "disagree" for k in sorted(common)]
            lb = ["agree" if b["ratings"][k]["verifier_validity"] == "agree"
                  else "disagree" for k in sorted(common)]
            pair_kappas.append({
                "pair": [a["annotator_id"], b["annotator_id"]],
                "n_common": len(common),
                "kappa": cohen_kappa(la, lb),
                "raw_agreement_pct": _percent(
                    sum(1 for x, y in zip(la, lb) if x == y), len(la)
                ),
            })

    # --- retained disagreements -----------------------------------------------
    by_key_responses: Dict[str, List[Tuple[str, Dict[str, Any]]]] = defaultdict(list)
    for resp in responses:
        for task_key, v in resp["ratings"].items():
            if high_confidence_only and v.get("confidence", "high") == "low":
                continue
            by_key_responses[task_key].append((resp["annotator_id"], v))

    retained: List[Dict[str, Any]] = []
    for task_key, lst in by_key_responses.items():
        any_disagree = any(v["verifier_validity"] != "agree" for _, v in lst)
        cross_split = len({v["verifier_validity"] == "agree" for _, v in lst}) > 1
        if any_disagree:
            retained.append({
                "task_key": task_key,
                "benchmark": meta_by_key.get(task_key, {}).get("benchmark", "?"),
                "operator": meta_by_key.get(task_key, {}).get("operator", "?"),
                "cross_annotator_split": cross_split,
                "ratings": [
                    {
                        "annotator_id": aid,
                        "naturalness": v["naturalness"],
                        "verifier_validity": v["verifier_validity"],
                        "notes": v.get("notes", ""),
                    }
                    for aid, v in lst
                ],
            })

    return {
        "n_annotators": n_annot,
        "high_confidence_only": high_confidence_only,
        "per_annotator": per_annot,
        "pooled": pooled,
        "per_cell": cell_summary,
        "pair_kappas": pair_kappas,
        "retained_disagreements": retained,
        "retained_disagreement_pct": _percent(
            len(retained), len(by_key_responses) or 1
        ),
        "n_unique_tasks_rated": len(by_key_responses),
    }


def fmt_pct(x: float) -> str:
    return f"{x:.1f}%" if not math.isnan(x) else "n/a"


def fmt_kappa(x: float) -> str:
    return f"{x:.2f}" if not math.isnan(x) else "n/a"


def write_summary_md(summary: Dict[str, Any], path: Path) -> None:
    lines: List[str] = []
    lines.append("# Human / expert calibration summary")
    lines.append("")
    lines.append(f"- Annotators: **{summary['n_annotators']}**")
    lines.append(f"- Tasks rated (any annotator): **{summary['n_unique_tasks_rated']}**")
    lines.append(f"- High-confidence-only filter applied: "
                 f"**{summary['high_confidence_only']}**")
    lines.append("")
    lines.append("## Headline (paper Table 18)")
    lines.append("")
    lines.append("| Audit item | Result |")
    lines.append("| --- | --- |")
    lines.append(f"| Task naturalness (≥4 on 5-point Likert) | "
                 f"{fmt_pct(summary['pooled']['naturalness_ge4_pct'])} "
                 f"(n={summary['pooled']['n']}) |")
    lines.append(f"| Verifier–annotator agreement (`agree` rate) | "
                 f"{fmt_pct(summary['pooled']['verifier_agree_pct'])} "
                 f"(n={summary['pooled']['n']}) |")
    if summary["pair_kappas"]:
        kappas = [k["kappa"] for k in summary["pair_kappas"]
                  if not math.isnan(k["kappa"])]
        avg = sum(kappas) / len(kappas) if kappas else float("nan")
        lines.append(f"| Cohen's κ (annotator pair, mean over pairs) | "
                     f"{fmt_kappa(avg)} |")
    lines.append(f"| Retained disagreements | "
                 f"{fmt_pct(summary['retained_disagreement_pct'])} "
                 f"({len(summary['retained_disagreements'])} tasks) |")
    lines.append("")

    lines.append("## Per benchmark × operator")
    lines.append("")
    lines.append("| Cell | n | Naturalness ≥4 | Verifier agree |")
    lines.append("| --- | --- | --- | --- |")
    for cell, d in summary["per_cell"].items():
        lines.append(f"| `{cell}` | {d['n']} | "
                     f"{fmt_pct(d['naturalness_ge4_pct'])} | "
                     f"{fmt_pct(d['verifier_agree_pct'])} |")
    lines.append("")

    lines.append("## Per annotator")
    lines.append("")
    lines.append("| Annotator | n | Naturalness ≥4 | Verifier agree |")
    lines.append("| --- | --- | --- | --- |")
    for a in summary["per_annotator"]:
        lines.append(f"| `{a['annotator_id']}` | {a['n']} | "
                     f"{fmt_pct(a['naturalness_ge4_pct'])} | "
                     f"{fmt_pct(a['verifier_agree_pct'])} |")
    lines.append("")

    if summary["pair_kappas"]:
        lines.append("## Cohen's κ — annotator pairs")
        lines.append("")
        lines.append("| Pair | n shared | Raw agreement | κ |")
        lines.append("| --- | --- | --- | --- |")
        for p in summary["pair_kappas"]:
            lines.append(f"| {p['pair'][0]} × {p['pair'][1]} | "
                         f"{p['n_common']} | "
                         f"{fmt_pct(p['raw_agreement_pct'])} | "
                         f"{fmt_kappa(p['kappa'])} |")
        lines.append("")

    lines.append("## Verifier-validity label distribution (pooled)")
    lines.append("")
    lines.append("| Label | Count |")
    lines.append("| --- | --- |")
    for lbl, cnt in summary["pooled"]["verifier_label_counts"].items():
        lines.append(f"| `{lbl}` | {cnt} |")
    lines.append("")

    path.write_text("\n".join(lines), encoding="utf-8")


def write_disagreements_md(summary: Dict[str, Any], path: Path) -> None:
    lines: List[str] = ["# Retained disagreements", ""]
    lines.append(f"Total: **{len(summary['retained_disagreements'])}** tasks "
                 f"({fmt_pct(summary['retained_disagreement_pct'])} of rated tasks).")
    lines.append("")
    for item in summary["retained_disagreements"]:
        lines.append(f"## `{item['task_key']}`")
        lines.append("")
        lines.append(f"- benchmark: `{item['benchmark']}`")
        lines.append(f"- operator: `{item['operator']}`")
        lines.append(f"- cross-annotator split: **{item['cross_annotator_split']}**")
        lines.append("")
        for r in item["ratings"]:
            lines.append(f"### Annotator `{r['annotator_id']}`")
            lines.append("")
            lines.append(f"- naturalness: **{r['naturalness']}**")
            lines.append(f"- verifier_validity: **{r['verifier_validity']}**")
            if r["notes"]:
                lines.append(f"- notes: {r['notes']}")
            lines.append("")
    path.write_text("\n".join(lines), encoding="utf-8")


def write_per_annotator_csv(summary: Dict[str, Any], path: Path) -> None:
    with path.open("w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["annotator_id", "n", "naturalness_ge4_pct", "verifier_agree_pct"])
        for a in summary["per_annotator"]:
            w.writerow([a["annotator_id"], a["n"],
                        f"{a['naturalness_ge4_pct']:.2f}",
                        f"{a['verifier_agree_pct']:.2f}"])


def main() -> int:
    parser = argparse.ArgumentParser(description="Aggregate audit responses.")
    parser.add_argument("--responses-dir", type=Path, default=DEFAULT_RESPONSES)
    parser.add_argument("--tasks-dir", type=Path, default=DEFAULT_TASKS)
    parser.add_argument("--results-dir", type=Path, default=DEFAULT_RESULTS)
    parser.add_argument("--high-confidence-only", action="store_true",
                        help="Exclude ratings with confidence='low' from headlines.")
    args = parser.parse_args()

    args.results_dir.mkdir(parents=True, exist_ok=True)

    try:
        responses = collect_responses(args.responses_dir)
    except RuntimeError as exc:
        sys.stderr.write(f"[aggregate] {exc}\n")
        return 2

    manifest = load_manifest(args.tasks_dir)
    if manifest is None:
        sys.stderr.write(
            f"[aggregate] note: no manifest at {args.tasks_dir}/manifest.json; "
            "per-cell breakdowns will be missing.\n"
        )

    summary = aggregate(
        responses=responses,
        manifest=manifest,
        high_confidence_only=args.high_confidence_only,
    )

    summary_json = args.results_dir / "summary.json"
    summary_md = args.results_dir / "summary.md"
    disagreements_md = args.results_dir / "disagreements.md"
    per_annot_csv = args.results_dir / "per_annotator.csv"

    with summary_json.open("w", encoding="utf-8") as fh:
        json.dump(summary, fh, ensure_ascii=False, indent=2)
    write_summary_md(summary, summary_md)
    write_disagreements_md(summary, disagreements_md)
    write_per_annotator_csv(summary, per_annot_csv)

    print("=" * 62)
    print("Human / expert calibration — pooled headline")
    print("=" * 62)
    print(f"  n annotators        : {summary['n_annotators']}")
    print(f"  n ratings (pooled)  : {summary['pooled']['n']}")
    print(f"  naturalness ≥ 4     : {fmt_pct(summary['pooled']['naturalness_ge4_pct'])}")
    print(f"  verifier agree      : {fmt_pct(summary['pooled']['verifier_agree_pct'])}")
    if summary["pair_kappas"]:
        kappas = [k["kappa"] for k in summary["pair_kappas"]
                  if not math.isnan(k["kappa"])]
        avg = sum(kappas) / len(kappas) if kappas else float("nan")
        print(f"  Cohen's κ (mean)    : {fmt_kappa(avg)}")
    print(f"  retained disagree   : {fmt_pct(summary['retained_disagreement_pct'])} "
          f"({len(summary['retained_disagreements'])} tasks)")
    print("-" * 62)
    print(f"  wrote: {summary_json}")
    print(f"  wrote: {summary_md}")
    print(f"  wrote: {disagreements_md}")
    print(f"  wrote: {per_annot_csv}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
