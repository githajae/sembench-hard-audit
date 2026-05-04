#!/usr/bin/env python3
"""Build the 120-task human audit set for SemBench-Hard Appendix D.

Samples 30 hard tasks per benchmark, stratified across the four
operators (Filter, Join, Map, Rank). The sample is deterministic given
a seed so two annotators reviewing the same kit see the same tasks.

Output layout:

    human_audit/
        tasks/
            manifest.json
            <benchmark>/NN_<operator>_<key>.json   # raw task object
            <benchmark>/NN_<operator>_<key>.md     # placeholder; filled by render_tasks.py

Usage (run from anywhere; paths are resolved relative to the repo
root):

    python scripts/build_tasks.py                # default seed 20260504
    python scripts/build_tasks.py --seed 42
    python scripts/build_tasks.py --dry-run      # skip writing files
    python scripts/build_tasks.py --benchmarks scifact contractnli

"""
from __future__ import annotations

import argparse
import json
import random
import sys
from pathlib import Path
from typing import Any, Callable, Dict, List, Tuple

# --- locate the repo and add code/ to sys.path -------------------------------
HERE = Path(__file__).resolve()
KIT_ROOT = HERE.parent.parent             # human_audit/
REPO_ROOT = KIT_ROOT.parent               # SEMBENCH-HARD/
CODE_ROOT = REPO_ROOT / "code"

if not CODE_ROOT.exists():
    sys.stderr.write(
        f"[build_tasks] could not find {CODE_ROOT}. Run this script from "
        "inside a checkout of the SemBench-Hard repo.\n"
    )
    sys.exit(2)

sys.path.insert(0, str(CODE_ROOT))

# These imports require the SemBench-Hard data files to be present.
# They will raise RuntimeError with a useful message if not.
try:
    from benchmarks.section_5_1 import (  # type: ignore
        default_split_for_benchmark,
        load_contractnli_hard_filter_tasks,
        load_contractnli_hard_join_tasks,
        load_contractnli_hard_map_tasks,
        load_contractnli_hard_rank_tasks,
        load_scifact_hard_filter_tasks,
        load_scifact_hard_join_tasks,
        load_scifact_hard_map_tasks,
        load_scifact_hard_rank_tasks,
        load_swebench_hard_filter_tasks,
        load_swebench_hard_join_tasks,
        load_swebench_hard_map_tasks,
        load_swebench_hard_rank_tasks,
        load_wdc_hard_filter_tasks,
        load_wdc_hard_join_tasks,
        load_wdc_hard_map_tasks,
        load_wdc_hard_rank_tasks,
        task_key_for_task,
    )
except Exception as exc:  # pragma: no cover - import diagnostic only
    sys.stderr.write(
        "[build_tasks] failed to import benchmarks.section_5_1.\n"
        f"  reason: {exc!r}\n"
        "  hint: make sure the repo's `code/` directory is intact and the "
        "raw datasets have been set up via scripts/setup_data.py.\n"
    )
    raise

# --- registry ----------------------------------------------------------------
# Each loader returns a list of dicts. We treat the loader's full output as
# the *pool* from which we sample N tasks per (benchmark, operator).
# Setting `max_examples` to None pulls the entire pool; the script uses an
# explicit `pool_cap` to bound memory while still giving the seeded sampler
# plenty of variety.

LoaderFn = Callable[[str, int], List[Dict[str, Any]]]

LOADERS: Dict[str, Dict[str, LoaderFn]] = {
    "scifact": {
        "filter": load_scifact_hard_filter_tasks,
        "join":   load_scifact_hard_join_tasks,
        "map":    load_scifact_hard_map_tasks,
        "rank":   load_scifact_hard_rank_tasks,
    },
    "contractnli": {
        "filter": load_contractnli_hard_filter_tasks,
        "join":   load_contractnli_hard_join_tasks,
        "map":    load_contractnli_hard_map_tasks,
        "rank":   load_contractnli_hard_rank_tasks,
    },
    "wdc_products": {
        "filter": load_wdc_hard_filter_tasks,
        "join":   load_wdc_hard_join_tasks,
        "map":    load_wdc_hard_map_tasks,
        "rank":   load_wdc_hard_rank_tasks,
    },
    "swebench_verified": {
        "filter": load_swebench_hard_filter_tasks,
        "join":   load_swebench_hard_join_tasks,
        "map":    load_swebench_hard_map_tasks,
        "rank":   load_swebench_hard_rank_tasks,
    },
}

OPERATORS = ("filter", "join", "map", "rank")
BENCHMARKS = tuple(LOADERS.keys())

# 30 / 4 operators = 8, 8, 7, 7 (filter, join, map, rank).
QUOTA_PER_OPERATOR: Dict[str, int] = {"filter": 8, "join": 8, "map": 7, "rank": 7}
TASKS_PER_BENCHMARK = sum(QUOTA_PER_OPERATOR.values())  # 30


def _safe_key(s: str) -> str:
    """Make a string safe for use in filenames."""
    return "".join(c if c.isalnum() or c in ("-", "_") else "_" for c in str(s))[:80]


def _task_family(operator: str) -> str:
    return f"hard_{operator}"


def sample_tasks(
    benchmark: str,
    operator: str,
    seed: int,
    quota: int,
    pool_cap: int,
    split: str,
) -> List[Dict[str, Any]]:
    """Pull a hard-task pool and sample `quota` tasks deterministically."""
    loader = LOADERS[benchmark][operator]
    pool = loader(split, max_examples=pool_cap)
    if not pool:
        raise RuntimeError(
            f"loader for {benchmark}/{operator} returned 0 tasks "
            f"(split={split}, cap={pool_cap})"
        )
    if len(pool) < quota:
        sys.stderr.write(
            f"[build_tasks] warning: pool for {benchmark}/{operator} "
            f"has only {len(pool)} tasks (< quota {quota}); using all.\n"
        )
        return list(pool)
    rng = random.Random(f"{seed}/{benchmark}/{operator}")
    return rng.sample(list(pool), quota)


def build_one_benchmark(
    benchmark: str,
    seed: int,
    pool_cap: int,
    split: str,
) -> List[Tuple[str, str, Dict[str, Any]]]:
    """Sample 30 tasks for one benchmark; returns list of (operator, key, task)."""
    out: List[Tuple[str, str, Dict[str, Any]]] = []
    for operator in OPERATORS:
        sampled = sample_tasks(
            benchmark=benchmark,
            operator=operator,
            seed=seed,
            quota=QUOTA_PER_OPERATOR[operator],
            pool_cap=pool_cap,
            split=split,
        )
        for task in sampled:
            family = _task_family(operator)
            try:
                key = task_key_for_task(benchmark, family, task)
            except Exception:
                # Fallback: synthesize a key from a few common id fields.
                fallback_id = (
                    task.get("instance_id")
                    or task.get("pair_id")
                    or task.get("task_id")
                    or task.get("hypothesis_key")
                    or task.get("doc_id")
                    or task.get("claim_id")
                    or "unknown"
                )
                key = f"{family}/{fallback_id}"
            out.append((operator, key, task))
    return out


def write_outputs(
    bench_results: Dict[str, List[Tuple[str, str, Dict[str, Any]]]],
    tasks_root: Path,
    seed: int,
    split_per_benchmark: Dict[str, str],
) -> Dict[str, Any]:
    """Write per-task .json files and a manifest. Returns the manifest dict."""
    tasks_root.mkdir(parents=True, exist_ok=True)
    manifest_entries: List[Dict[str, Any]] = []
    for benchmark, items in bench_results.items():
        bench_dir = tasks_root / benchmark
        bench_dir.mkdir(parents=True, exist_ok=True)
        for idx, (operator, key, task) in enumerate(items, start=1):
            safe = _safe_key(key)
            stem = f"{idx:02d}_{operator}_{safe}"
            json_path = bench_dir / f"{stem}.json"
            with json_path.open("w", encoding="utf-8") as fh:
                json.dump(
                    {
                        "benchmark": benchmark,
                        "operator": operator,
                        "task_family": _task_family(operator),
                        "task_key": key,
                        "task": task,
                    },
                    fh,
                    ensure_ascii=False,
                    indent=2,
                    sort_keys=False,
                    default=str,
                )
            manifest_entries.append(
                {
                    "benchmark": benchmark,
                    "operator": operator,
                    "task_family": _task_family(operator),
                    "task_key": key,
                    "stem": stem,
                    "json": str(json_path.relative_to(tasks_root.parent)),
                    "md": str((bench_dir / f"{stem}.md").relative_to(tasks_root.parent)),
                }
            )
    manifest = {
        "seed": seed,
        "splits": split_per_benchmark,
        "tasks_per_benchmark": TASKS_PER_BENCHMARK,
        "quota_per_operator": dict(QUOTA_PER_OPERATOR),
        "benchmarks": list(bench_results.keys()),
        "n_total": len(manifest_entries),
        "entries": manifest_entries,
    }
    manifest_path = tasks_root / "manifest.json"
    with manifest_path.open("w", encoding="utf-8") as fh:
        json.dump(manifest, fh, ensure_ascii=False, indent=2)
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the 120-task human audit set.")
    parser.add_argument("--seed", type=int, default=20260504,
                        help="Sampling seed (default: 20260504, matches paper).")
    parser.add_argument("--pool-cap", type=int, default=2000,
                        help="Cap on tasks pulled per loader call (default 2000).")
    parser.add_argument("--benchmarks", nargs="*", default=list(BENCHMARKS),
                        choices=BENCHMARKS,
                        help="Subset of benchmarks to build (default: all 4).")
    parser.add_argument("--dry-run", action="store_true",
                        help="Sample tasks but don't write any files.")
    parser.add_argument("--out", type=Path, default=KIT_ROOT / "tasks",
                        help="Output directory (default human_audit/tasks).")
    args = parser.parse_args()

    print(f"[build_tasks] seed={args.seed}  benchmarks={args.benchmarks}")
    print(f"[build_tasks] tasks per benchmark: {TASKS_PER_BENCHMARK} "
          f"({QUOTA_PER_OPERATOR})")
    print(f"[build_tasks] writing to: {args.out}")

    bench_results: Dict[str, List[Tuple[str, str, Dict[str, Any]]]] = {}
    split_per_benchmark: Dict[str, str] = {}
    for benchmark in args.benchmarks:
        split = default_split_for_benchmark(benchmark)
        split_per_benchmark[benchmark] = split
        print(f"[build_tasks] {benchmark}: split={split}")
        try:
            items = build_one_benchmark(
                benchmark=benchmark,
                seed=args.seed,
                pool_cap=args.pool_cap,
                split=split,
            )
        except Exception as exc:
            sys.stderr.write(
                f"[build_tasks] failed to build {benchmark}: {exc}\n"
                "  hint: ensure raw data is set up (`python code/scripts/setup_data.py`).\n"
            )
            return 3
        per_op_counts = {op: 0 for op in OPERATORS}
        for op, _, _ in items:
            per_op_counts[op] += 1
        print(f"[build_tasks] {benchmark}: sampled {len(items)} tasks "
              f"({per_op_counts})")
        bench_results[benchmark] = items

    if args.dry_run:
        print("[build_tasks] --dry-run: skipping file writes.")
        total = sum(len(v) for v in bench_results.values())
        print(f"[build_tasks] dry-run total tasks: {total}")
        return 0

    manifest = write_outputs(
        bench_results=bench_results,
        tasks_root=args.out,
        seed=args.seed,
        split_per_benchmark=split_per_benchmark,
    )
    print(f"[build_tasks] wrote {manifest['n_total']} task .json files "
          f"and manifest at {args.out / 'manifest.json'}.")
    print("[build_tasks] next: run `python scripts/render_tasks.py` to "
          "generate the .md task pages.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
