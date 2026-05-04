#!/usr/bin/env python3
"""Interactive CLI for the SemBench-Hard calibration audit.

This is the "딸깍 → annotation" path for users who want to run the
audit in a plain terminal. It iterates the manifest, shows each
un-rated task, prompts for a naturalness score (1-5) and a verifier
validity value, and writes the response into
`responses/<user>.json`.

A separate path exists for Cowork / Claude Code users — see
`CLAUDE.md`. That path is preferred because Claude can offer a
reasoned tentative rating before asking; this CLI only collects the
human's answer.

Usage:

    python scripts/annotate.py --user jaehyun
    python scripts/annotate.py --user jaehyun --start-from 9
    python scripts/annotate.py --user jaehyun --benchmark contractnli
    python scripts/annotate.py --user jaehyun --show-llm-prompt   # print
                                                                   # the
                                                                   # LLM
                                                                   # co-pilot
                                                                   # prompt
                                                                   # for
                                                                   # the
                                                                   # current
                                                                   # task

Stdlib only — no dependencies beyond Python 3.9+.
"""
from __future__ import annotations

import argparse
import json
import sys
import textwrap
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

HERE = Path(__file__).resolve()
KIT_ROOT = HERE.parent.parent
DEFAULT_TASKS = KIT_ROOT / "tasks"
DEFAULT_RESPONSES = KIT_ROOT / "responses"

VALID_VERIFIER = ("agree", "disagree_too_strict", "disagree_too_lax", "disagree_other")
VALID_CONF = ("high", "medium", "low")


def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def read_manifest(tasks_dir: Path) -> Dict[str, Any]:
    p = tasks_dir / "manifest.json"
    if not p.exists():
        sys.stderr.write(
            f"[annotate] no manifest at {p}. "
            "Run `python scripts/build_tasks.py` first, or unzip the kit.\n"
        )
        sys.exit(2)
    with p.open(encoding="utf-8") as fh:
        return json.load(fh)


def load_response(path: Path, user: str) -> Dict[str, Any]:
    if path.exists():
        with path.open(encoding="utf-8") as fh:
            data = json.load(fh)
        if "ratings" not in data:
            data["ratings"] = {}
        return data
    return {
        "annotator_id": user,
        "started_at": now_iso(),
        "finished_at": None,
        "ratings": {},
    }


def save_response(path: Path, data: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data["finished_at"] = now_iso()
    with path.open("w", encoding="utf-8") as fh:
        json.dump(data, fh, ensure_ascii=False, indent=2)


def prompt_str(prompt: str, default: Optional[str] = None,
               valid: Optional[tuple] = None) -> str:
    suffix = f" [{default}]" if default is not None else ""
    while True:
        try:
            raw = input(f"{prompt}{suffix} ").strip()
        except EOFError:
            print()
            sys.exit(0)
        if not raw and default is not None:
            return default
        if valid is None:
            return raw
        if raw in valid:
            return raw
        print(f"  → must be one of: {', '.join(valid)}")


def prompt_int(prompt: str, lo: int, hi: int,
               default: Optional[int] = None) -> int:
    suffix = f" [{default}]" if default is not None else ""
    while True:
        try:
            raw = input(f"{prompt}{suffix} ").strip()
        except EOFError:
            print()
            sys.exit(0)
        if not raw and default is not None:
            return default
        try:
            val = int(raw)
        except ValueError:
            print(f"  → must be an integer in [{lo},{hi}]")
            continue
        if lo <= val <= hi:
            return val
        print(f"  → must be an integer in [{lo},{hi}]")


def render_md_to_terminal(md_path: Path, max_width: int = 88) -> None:
    """Print a Markdown task page to the terminal with mild formatting."""
    text = md_path.read_text(encoding="utf-8")
    out_lines: List[str] = []
    for line in text.splitlines():
        # Collapse the HTML <details> blocks (used in "Other fields") to
        # a single hint so the terminal output is short.
        if line.startswith("<details>") or line.startswith("</details>"):
            continue
        if line.startswith("<summary>"):
            stripped = line.replace("<summary>", "").replace("</summary>", "")
            out_lines.append(f"  · {stripped}")
            continue
        out_lines.append(line)
    out = "\n".join(out_lines)
    # Fold blockquotes a little more tightly.
    print(out)


def llm_prompt_for_task(task_obj: Dict[str, Any]) -> str:
    """Return the LLM_PROMPT.md prompt body with this task's JSON inlined."""
    template = (KIT_ROOT / "LLM_PROMPT.md").read_text(encoding="utf-8")
    # The prompt template has a `<<<TASK_JSON>>>` placeholder.
    rendered = template.replace(
        "<<<TASK_JSON>>>",
        json.dumps(task_obj, ensure_ascii=False, indent=2, default=str),
    )
    return rendered


def collect_one_rating(
    *,
    md_path: Path,
    json_path: Path,
    show_llm_prompt: bool,
) -> Optional[Dict[str, Any]]:
    print()
    print("=" * 88)
    render_md_to_terminal(md_path)
    print("=" * 88)
    print()

    if show_llm_prompt:
        with json_path.open(encoding="utf-8") as fh:
            task_obj = json.load(fh)
        print()
        print("---- LLM CO-PILOT PROMPT (paste this into Claude / ChatGPT) ----")
        print(llm_prompt_for_task(task_obj))
        print("---- END PROMPT ----")
        print()

    # Loop in case the user wants to redo their last answer.
    while True:
        nat = prompt_int(
            "  Q1 — Naturalness (1=broken, 3=borderline, 5=fully natural):",
            lo=1, hi=5,
        )
        val = prompt_str(
            f"  Q2 — Verifier validity (one of: {', '.join(VALID_VERIFIER)}):",
            default="agree",
            valid=VALID_VERIFIER,
        )
        conf = prompt_str(
            "  Confidence (high/medium/low):",
            default="medium",
            valid=VALID_CONF,
        )
        notes = prompt_str(
            "  Notes (Enter to skip, required if Q2 != agree):",
            default="",
        )
        if val != "agree" and not notes.strip():
            print("  → Q2 is a disagree value; please provide a short note.")
            continue
        confirm = prompt_str(
            f"  Confirm (Enter=yes, 'r'=redo, 's'=skip & save 'skipped' marker, 'q'=quit):",
            default="",
            valid=("", "r", "s", "q"),
        )
        if confirm == "r":
            print("  Redoing this task.")
            continue
        if confirm == "s":
            return {
                "naturalness": 3,
                "verifier_validity": "disagree_other",
                "confidence": "low",
                "notes": "skipped via annotate.py",
            }
        if confirm == "q":
            return None
        return {
            "naturalness": nat,
            "verifier_validity": val,
            "confidence": conf,
            "notes": notes,
        }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Interactive audit annotation CLI (terminal).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent("""\
            Examples:
              # Resume / start your session
              python scripts/annotate.py --user jaehyun

              # Re-rate just one task
              python scripts/annotate.py --user jaehyun --only contract:91/hypothesis:nda-12

              # Print the LLM co-pilot prompt before each task
              python scripts/annotate.py --user jaehyun --show-llm-prompt
        """),
    )
    parser.add_argument("--user", required=True,
                        help="Annotator id; writes to responses/<user>.json.")
    parser.add_argument("--tasks-dir", type=Path, default=DEFAULT_TASKS)
    parser.add_argument("--responses-dir", type=Path, default=DEFAULT_RESPONSES)
    parser.add_argument("--benchmark",
                        choices=("contractnli", "scifact",
                                 "wdc_products", "swebench_verified"),
                        help="Restrict to one benchmark this session.")
    parser.add_argument("--start-from", type=int, default=0,
                        help="Skip the first N tasks of the manifest.")
    parser.add_argument("--only", default=None,
                        help="Re-rate exactly this task_key; ignore others.")
    parser.add_argument("--show-llm-prompt", action="store_true",
                        help="Print the LLM co-pilot prompt before each task.")
    args = parser.parse_args()

    manifest = read_manifest(args.tasks_dir)
    entries = list(manifest["entries"])
    if args.benchmark:
        entries = [e for e in entries if e["benchmark"] == args.benchmark]
    response_path = args.responses_dir / f"{args.user}.json"
    response_data = load_response(response_path, args.user)
    rated = set(response_data["ratings"])

    if args.only:
        targets = [e for e in entries if e["task_key"] == args.only]
        if not targets:
            sys.stderr.write(f"[annotate] no entry with task_key={args.only}\n")
            return 2
        todo = targets
    else:
        todo = [e for e in entries[args.start_from:] if e["task_key"] not in rated]

    total = len(entries)
    done = sum(1 for e in entries if e["task_key"] in rated)
    print(f"\nWelcome, {args.user}.")
    print(f"  Manifest: {manifest.get('n_total','?')} tasks total "
          f"({len(entries)} after filters).")
    print(f"  Already rated by you: {done} / {total}.")
    print(f"  Remaining this run: {len(todo)}.")
    print(f"  Response file: {response_path}")
    print()
    if not todo:
        print("Nothing to do — every task in scope is already rated.")
        print("Run `python scripts/aggregate.py` to compute the summary.")
        return 0

    for i, entry in enumerate(todo, start=1):
        md_path = KIT_ROOT / entry["md"]
        json_path = KIT_ROOT / entry["json"]
        if not md_path.exists():
            sys.stderr.write(f"[annotate] missing {md_path}; skipping.\n")
            continue
        print(f"\n##### Task {i} of {len(todo)} this run "
              f"(global {entries.index(entry) + 1} / {total}) #####")
        print(f"  benchmark : {entry['benchmark']}")
        print(f"  operator  : {entry['operator']}")
        print(f"  task_key  : {entry['task_key']}")
        rating = collect_one_rating(
            md_path=md_path,
            json_path=json_path,
            show_llm_prompt=args.show_llm_prompt,
        )
        if rating is None:
            print("Quitting; progress saved.")
            break
        response_data["ratings"][entry["task_key"]] = rating
        save_response(response_path, response_data)
        print(f"  ✓ saved to {response_path}")

    print()
    print("Done with this session.")
    print(f"  Total rated by you: {len(response_data['ratings'])} / {total}.")
    print(f"  When you finish all 120, run: python scripts/aggregate.py")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
