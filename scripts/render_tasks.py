#!/usr/bin/env python3
"""Render audit task JSON files into annotator-friendly Markdown pages.

For every entry in `tasks/manifest.json`, write a sibling `.md` file
that lets an annotator answer Q1 (naturalness) and Q2 (verifier
validity) without reading the raw JSON.

The page layout is:

  1. Header (benchmark, operator, task_key)
  2. Key facts        - benchmark-aware, the inputs the model would
                        see plus the gold answer **with span /
                        sentence ids resolved to their text**.
  3. Verifier rule    - the contract being audited in Q2.
  4. Policy text      - the operator's instructions to the model.
  5. Other fields     - the remaining task object, truncated for
                        reference only.
  6. Audit questions  - the two questions and how to answer.

Usage:

    python scripts/render_tasks.py
    python scripts/render_tasks.py --tasks-dir /path/to/tasks
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Optional, Tuple

HERE = Path(__file__).resolve()
KIT_ROOT = HERE.parent.parent
DEFAULT_TASKS = KIT_ROOT / "tasks"

# Fields whose raw rendering is too long for the "Other fields" block;
# we truncate but keep a marker for the reader.
LARGE_FIELDS = {
    "body_sections",
    "paper_body",
    "document_text",
    "text",
    "abstract",
    "contract_text",
    "patch",
    "candidate_patch",
    "gold_patch",
    "issue_text",
    "test_patch",
    "left_text",
    "right_text",
    "candidates",
    "contract_spans",
    "candidate_clauses",
    "confuser_clauses",
    "confuser_offers",
}

# Fields rendered in the "Key facts" block; suppressed from "Other fields".
SUPPRESS_FROM_OTHER = {
    # contractnli
    "contract_spans",
    "candidate_clauses",
    "confuser_clauses",
    "candidate_span_ids",
    "gold_variants",
    "gold_label",
    "gold_basis",
    "gold_decisive_attributes",
    "gold_positive_span_ids",
    "hypothesis_text",
    "hypothesis_key",
    "span_id",
    "policy_text",
    "task_type",
    "top_k",
    # scifact
    "claim",
    "claim_text",
    "claim_id",
    "doc_id",
    "abstract_sentences",
    "accepted_sentence_id_variants",
    "gold_sentence_ids",
    # wdc
    "left_offer",
    "right_offer",
    "confuser_offers",
    "matched_attribute_hints",
    "conflict_attribute_hints",
    "pair_id",
    # swebench
    "instance_id",
    "issue_title",
    "issue_body",
    "candidates",
    "candidate_patches",
    "test_signal",
    "patched_files",
}

PREVIEW_CHARS = 1500
MAX_CONFUSERS_FULL = 5  # show this many confuser items un-truncated


# ---------------------------------------------------------------------------
# Verifier-rule templates per (benchmark, task_family). Each is a concise,
# faithful summary of what the strict verifier in code/benchmarks checks.
# Updated to match the actual gold fields (e.g. label/basis/decisive
# attributes for WDC Map, single (label, span_ids) tuple for ContractNLI
# Hard Join).
# ---------------------------------------------------------------------------
VERIFIER_RULES: Dict[str, Dict[str, str]] = {
    "scifact": {
        "hard_join": (
            "Output is `(label, sentence_ids)` over the abstract. "
            "Accept iff `label` matches the gold (`support` / `contradict` / "
            "`no_evidence`) AND `sentence_ids` (sorted, dedup'd, "
            "abstract-relative) equals one of the accepted variants exactly. "
            "Empty `sentence_ids` only valid for `no_evidence`."
        ),
        "hard_filter": (
            "Same `(label, sentence_ids)` tuple as Hard Join; the strict "
            "check is identical. Filter drops `no_evidence` downstream."
        ),
        "hard_map": (
            "Output is the structured map record (label + basis enum + "
            "citations). Accept iff every required field matches the gold "
            "exactly, citations are abstract-relative ids drawn from one of "
            "the accepted evidence variants, and the basis enum is "
            "consistent with the label."
        ),
        "hard_rank": (
            "Output is a ranked list of `sentence_ids` of length `top_k`. "
            "Accept iff each id is a valid abstract sentence id and the "
            "top-`k` set covers an accepted gold-evidence variant for the "
            "claim."
        ),
    },
    "contractnli": {
        "hard_join": (
            "Output is a binary label for the (candidate clause, hypothesis) "
            "pair: `evidence` if the candidate's `span_id` is the supporting "
            "evidence for the hypothesis under the gold annotation, else "
            "`not_evidence`. Accept iff `label` matches the gold."
        ),
        "hard_filter": (
            "Output is `(label, span_ids)` over the contract. Accept iff "
            "`label` matches the gold (`entailment` / `contradiction` / "
            "`not_mentioned`) AND `span_ids` equals one of the accepted "
            "gold-evidence variants. Empty `span_ids` only valid for "
            "`not_mentioned`."
        ),
        "hard_map": (
            "Output is the structured map record (label + basis + "
            "span_ids). Accept iff label matches gold, span_ids form an "
            "accepted variant, and the basis enum is consistent with span "
            "content (e.g. `direct_support` vs `exception_clause`)."
        ),
        "hard_rank": (
            "Output is a ranked list of `span_ids` of length `top_k`. "
            "Accept iff each id is a valid contract-span id and the top-`k` "
            "set contains every gold-positive span for the hypothesis."
        ),
    },
    "wdc_products": {
        "hard_join": (
            "Output is a binary match label for the offer pair. Accept iff "
            "`label` matches the gold (`match` / `no_match`)."
        ),
        "hard_filter": (
            "Same binary check as Hard Join; the strict verifier is "
            "identical."
        ),
        "hard_map": (
            "Output is `(label, basis, decisive_attributes)`. Accept iff "
            "`label` matches gold, `basis` enum matches gold "
            "(e.g. `same_core_product`, `variant_or_bundle_mismatch`), and "
            "`decisive_attributes` set equals the gold set."
        ),
        "hard_rank": (
            "Output is a ranked list of right-side offer ids of length "
            "`top_k`. Accept iff the top-`k` set contains the gold matching "
            "offer (and gold non-matches are not above it)."
        ),
    },
    "swebench_verified": {
        "hard_join": (
            "Output is a binary `(issue, candidate_patch)` label, with "
            "false-fix distractors of the form `<id>__falsefix`. Accept iff "
            "label matches gold for the candidate."
        ),
        "hard_filter": (
            "Output is a binary in/out decision for a candidate file with "
            "respect to the gold patch. Accept iff the file selection "
            "matches the gold patch's changed-file set under the operator's "
            "policy."
        ),
        "hard_map": (
            "Output is the structured patch-summary record (e.g. "
            "patched_files set + intent enum + test_signal). Accept iff "
            "each required field matches the gold under the canonicalisation "
            "rule."
        ),
        "hard_rank": (
            "Output is a ranked list of candidate patch ids of length "
            "`top_k`. Accept iff the top-`k` set contains the gold patch."
        ),
    },
}


# ---------------------------------------------------------------------------
# Helpers.
# ---------------------------------------------------------------------------
def truncate_blob(value: Any, limit: int = PREVIEW_CHARS) -> str:
    if isinstance(value, (dict, list)):
        try:
            text = json.dumps(value, ensure_ascii=False, indent=2, default=str)
        except TypeError:
            text = repr(value)
    else:
        text = str(value)
    if len(text) <= limit:
        return text
    return text[:limit].rstrip() + "\n... [truncated, full content in the .json file] ..."


def fmt_quote(text: str, limit: int = 1200) -> str:
    """Format a text blob as a Markdown blockquote."""
    text = str(text).strip()
    if len(text) > limit:
        text = text[:limit].rstrip() + " …"
    return "\n".join("> " + line for line in text.splitlines())


def spans_by_id(spans: Optional[List[Dict[str, Any]]]) -> Dict[int, str]:
    out: Dict[int, str] = {}
    for s in spans or []:
        try:
            out[int(s["span_id"])] = str(s.get("text", ""))
        except (KeyError, TypeError, ValueError):
            continue
    return out


def sentences_by_id(items: Optional[List[Any]]) -> Dict[int, str]:
    """SciFact abstracts are usually a flat list of strings; index them."""
    out: Dict[int, str] = {}
    if not items:
        return out
    for i, s in enumerate(items):
        if isinstance(s, dict) and "text" in s:
            out[int(s.get("sentence_id", i))] = str(s["text"])
        else:
            out[i] = str(s)
    return out


def _resolve_top_k(task: Dict[str, Any]) -> Optional[int]:
    for key in ("top_k", "k", "rank_k"):
        if key in task and isinstance(task[key], int):
            return task[key]
    # Common defaults baked into the benchmark builders.
    return None


# ---------------------------------------------------------------------------
# Benchmark-aware key-facts blocks.
# ---------------------------------------------------------------------------
def key_facts_contractnli(task: Dict[str, Any], family: str) -> str:
    parts: List[str] = []
    # Build a unified span_id -> text map from every available source.
    # Different ContractNLI task families ship different fields:
    #   - hard_filter / hard_map: `contract_spans` (full contract) + `confuser_clauses`
    #   - hard_join:              `span_text` (candidate only) + `confuser_clauses`
    #   - hard_rank:              `candidate_clauses` (id+text only)
    spans: Dict[int, str] = {}
    spans.update(spans_by_id(task.get("contract_spans")))
    spans.update(spans_by_id(task.get("candidate_clauses")))
    spans.update(spans_by_id(task.get("confuser_clauses")))
    if "span_id" in task and "span_text" in task:
        try:
            spans[int(task["span_id"])] = str(task["span_text"])
        except (TypeError, ValueError):
            pass

    hyp = task.get("hypothesis_text")
    if hyp:
        parts.append("**Hypothesis** (the claim about the contract):")
        parts.append("")
        parts.append(fmt_quote(hyp))
        parts.append("")

    if family == "hard_join":
        # The candidate is one specific clause; its text is the most
        # important thing on the page.
        cand_id = task.get("span_id")
        cand_text = task.get("span_text")
        if cand_text is None and cand_id is not None:
            try:
                cand_text = spans.get(int(cand_id))
            except (TypeError, ValueError):
                cand_text = None
        if cand_text:
            parts.append(f"**Candidate clause** (`span_id = {cand_id}`):")
            parts.append("")
            parts.append(fmt_quote(cand_text))
            parts.append("")
        else:
            parts.append(f"*(candidate clause text not available; "
                         f"span_id = {cand_id})*")
            parts.append("")
        gold_label = task.get("gold_label")
        if gold_label is not None:
            parts.append(f"**Gold label:** `{gold_label}`")
            parts.append("")

    elif family in {"hard_filter", "hard_map"}:
        gold_label = task.get("gold_label")
        if gold_label is not None:
            parts.append(f"**Gold label:** `{gold_label}`")
        gold_basis = task.get("gold_basis")
        if gold_basis is not None:
            parts.append(f"**Gold basis:** `{gold_basis}`")
        parts.append("")
        gv = task.get("gold_variants") or []
        if gv:
            parts.append("**Gold-evidence variants** (each variant is one "
                         "accepted set of `span_ids`; the verifier accepts "
                         "any single variant exactly):")
            parts.append("")
            for vi, variant in enumerate(gv, start=1):
                parts.append(f"- Variant {vi}: `span_ids = {variant}`")
                for sid in variant or []:
                    try:
                        text = spans.get(int(sid), "(span text not in task)")
                    except (TypeError, ValueError):
                        text = "(invalid span id)"
                    # Show gold spans in full (no truncation): they are
                    # the only evidence for Q2.
                    parts.append(f"  > {text.strip()}")
                if not variant:
                    parts.append("  > *(empty: only valid for `not_mentioned`)*")
            parts.append("")

    elif family == "hard_rank":
        top_k = _resolve_top_k(task) or 3
        parts.append(f"**`top_k` (rank length the verifier checks):** `{top_k}`")
        parts.append("")
        gold_pos = task.get("gold_positive_span_ids") or []
        parts.append(f"**Gold-positive `span_ids`** (must appear in top-{top_k}):")
        for sid in gold_pos:
            try:
                text = spans.get(int(sid), "(span text not in task)")
            except (TypeError, ValueError):
                text = "(invalid span id)"
            # Gold spans in full so the annotator can decide whether the
            # gold positive really should be top-k.
            parts.append(f"- `span_id = {sid}` — {text.strip()}")
        parts.append("")

    # Candidate / confuser preview (un-truncated for the first few)
    confusers = task.get("confuser_clauses") or task.get("candidate_clauses")
    if confusers and family != "hard_rank":
        parts.append(f"**Confuser / candidate clauses (first {MAX_CONFUSERS_FULL} shown in full):**")
        parts.append("")
        for c in confusers[:MAX_CONFUSERS_FULL]:
            parts.append(f"- `span_id = {c.get('span_id')}` — {str(c.get('text','')).strip()[:600]}")
        if len(confusers) > MAX_CONFUSERS_FULL:
            parts.append(f"- *…and {len(confusers) - MAX_CONFUSERS_FULL} more "
                         "(see the .json for the complete list).*")
        parts.append("")

    return "\n".join(parts)


def key_facts_scifact(task: Dict[str, Any], family: str) -> str:
    parts: List[str] = []
    claim_text = task.get("claim_text") or task.get("claim")
    if isinstance(claim_text, dict):
        claim_text = claim_text.get("claim") or claim_text.get("text")
    if claim_text:
        parts.append("**Claim:**")
        parts.append("")
        parts.append(fmt_quote(str(claim_text)))
        parts.append("")

    abstract = task.get("abstract_sentences") or task.get("abstract")
    sent_text = sentences_by_id(abstract)
    if sent_text:
        parts.append("**Abstract sentences (the only evidence the verifier accepts):**")
        parts.append("")
        for sid in sorted(sent_text):
            parts.append(f"- `sentence_id = {sid}` — {sent_text[sid][:400].strip()}")
        parts.append("")

    if family in {"hard_join", "hard_filter", "hard_map"}:
        gold_label = task.get("gold_label")
        if gold_label is not None:
            parts.append(f"**Gold label:** `{gold_label}`")
            parts.append("")
        variants = task.get("accepted_sentence_id_variants") or []
        if variants:
            parts.append("**Accepted `sentence_ids` variants** "
                         "(verifier accepts any single variant exactly):")
            parts.append("")
            for vi, v in enumerate(variants, start=1):
                resolved = "; ".join(
                    f"({sid}) {sent_text.get(sid, '?')[:200].strip()}"
                    for sid in (v or [])
                ) or "(empty: valid only for `no_evidence`)"
                parts.append(f"- Variant {vi}: `{v}` — {resolved}")
            parts.append("")

    if family == "hard_rank":
        top_k = _resolve_top_k(task) or 3
        parts.append(f"**`top_k` (rank length):** `{top_k}`")
        gold = task.get("gold_evidence") or task.get("accepted_sentence_id_variants")
        if gold:
            parts.append("**Gold evidence (any single variant covers acceptance):**")
            parts.append("")
            parts.append(f"```\n{json.dumps(gold, indent=2, default=str)[:1200]}\n```")
            parts.append("")

    return "\n".join(parts)


def key_facts_wdc(task: Dict[str, Any], family: str) -> str:
    parts: List[str] = []
    left = task.get("left_offer")
    right = task.get("right_offer")

    if left or right:
        parts.append("**Offer pair under audit:**")
        parts.append("")
    if left:
        parts.append(f"- **Left** (id `{left.get('id')}`, brand "
                     f"`{left.get('brand')}`, "
                     f"`{left.get('price_currency')} {left.get('price')}`)")
        parts.append(f"  > **Title:** {left.get('title','')}")
        if left.get("description"):
            parts.append(f"  > **Description:** {str(left['description'])[:400]}")
    if right:
        parts.append(f"- **Right** (id `{right.get('id')}`, brand "
                     f"`{right.get('brand')}`, "
                     f"`{right.get('price_currency')} {right.get('price')}`)")
        parts.append(f"  > **Title:** {right.get('title','')}")
        if right.get("description"):
            parts.append(f"  > **Description:** {str(right['description'])[:400]}")
    parts.append("")

    gold_label = task.get("gold_label")
    if gold_label is not None:
        parts.append(f"**Gold label:** `{gold_label}`")
    gold_basis = task.get("gold_basis")
    if gold_basis is not None:
        parts.append(f"**Gold basis:** `{gold_basis}`")
    gold_attrs = task.get("gold_decisive_attributes")
    if gold_attrs is not None:
        parts.append(f"**Gold decisive attributes:** `{gold_attrs}`")
    if gold_label is not None or gold_basis is not None:
        parts.append("")

    if family == "hard_rank":
        top_k = _resolve_top_k(task) or 3
        parts.append(f"**`top_k` (rank length):** `{top_k}`")
        parts.append("")

    confusers = task.get("confuser_offers") or []
    if confusers:
        parts.append(f"**Confuser offers (first {MAX_CONFUSERS_FULL} shown):**")
        parts.append("")
        for c in confusers[:MAX_CONFUSERS_FULL]:
            parts.append(f"- id `{c.get('id')}`, brand `{c.get('brand')}` — "
                         f"{str(c.get('title',''))[:200]}")
        if len(confusers) > MAX_CONFUSERS_FULL:
            parts.append(f"- *…and {len(confusers) - MAX_CONFUSERS_FULL} more.*")
        parts.append("")

    return "\n".join(parts)


def key_facts_swebench(task: Dict[str, Any], family: str) -> str:
    parts: List[str] = []
    inst = task.get("instance_id")
    if inst:
        parts.append(f"**SWE-bench instance:** `{inst}`")
    title = task.get("issue_title")
    body = task.get("issue_body") or task.get("issue_text")
    if title:
        parts.append(f"**Issue title:** {title}")
    if body:
        parts.append("")
        parts.append("**Issue body (truncated):**")
        parts.append("")
        parts.append(fmt_quote(str(body)[:1200]))
        parts.append("")
    gold_label = task.get("gold_label")
    if gold_label is not None:
        parts.append(f"**Gold label:** `{gold_label}`")
        parts.append("")

    if family == "hard_join":
        cand = task.get("candidate_patch") or task.get("patch")
        if cand:
            parts.append("**Candidate patch (first 800 chars):**")
            parts.append("")
            parts.append("```diff\n" + str(cand)[:800].strip() + "\n```")
            parts.append("")

    if family == "hard_rank":
        top_k = _resolve_top_k(task) or 3
        parts.append(f"**`top_k`:** `{top_k}`")
        parts.append("")

    return "\n".join(parts)


KEY_FACTS = {
    "contractnli": key_facts_contractnli,
    "scifact": key_facts_scifact,
    "wdc_products": key_facts_wdc,
    "swebench_verified": key_facts_swebench,
}


def _is_gold_field(name: str) -> bool:
    n = name.lower()
    return n.startswith("gold_") or n.startswith("accepted_") or n in {"label"}


def _is_policy_field(name: str) -> bool:
    return name.lower() in {"policy_text", "policy", "instructions"}


# ---------------------------------------------------------------------------
# Top-level page renderer.
# ---------------------------------------------------------------------------
def render_task_md(entry: Dict[str, Any], task_obj: Dict[str, Any]) -> str:
    benchmark = entry["benchmark"]
    operator = entry["operator"]
    family = entry["task_family"]
    key = entry["task_key"]
    stem = entry["stem"]

    rule = (VERIFIER_RULES.get(benchmark, {}).get(family)
            or "(no rule template; see verifier source in code/benchmarks)")

    task = task_obj.get("task", task_obj)
    key_facts_fn = KEY_FACTS.get(benchmark)

    # "Other fields" — everything not already shown in Key facts / Policy /
    # Verifier rule, truncated for reference.
    policy_text = task.get("policy_text") or task.get("policy")
    other_fields_md: List[str] = []
    for field in sorted(task.keys()):
        if field in SUPPRESS_FROM_OTHER:
            continue
        if _is_policy_field(field) or _is_gold_field(field):
            continue
        value = task[field]
        if field in LARGE_FIELDS or (isinstance(value, str) and len(value) > PREVIEW_CHARS):
            other_fields_md.append(
                f"<details><summary><code>{field}</code> (truncated)"
                f"</summary>\n\n```\n{truncate_blob(value)}\n```\n\n</details>\n"
            )
        else:
            other_fields_md.append(
                f"<details><summary><code>{field}</code></summary>\n\n"
                f"```\n{truncate_blob(value, 600)}\n```\n\n</details>\n"
            )

    parts: List[str] = []
    parts.append(f"# Audit task — {benchmark} / {operator}")
    parts.append("")
    parts.append(f"**task_key:** `{key}`  ")
    parts.append(f"**task_family:** `{family}`  ")
    parts.append(f"**file stem:** `{stem}`")
    parts.append("")
    parts.append("> Read this page top-to-bottom, then write your two ratings "
                 "into `responses/<your_name>.json` under the key shown above. "
                 "See `PROTOCOL.md` for the rubric.")
    parts.append("")
    parts.append("---")
    parts.append("")
    parts.append("## Key facts")
    parts.append("")
    parts.append("*(The inputs the model would see, plus the gold answer "
                 "with span / sentence ids resolved to their text. "
                 "These are the facts you actually need to rate Q1 and Q2.)*")
    parts.append("")
    if key_facts_fn is not None:
        block = key_facts_fn(task, family)
        if block.strip():
            parts.append(block)
        else:
            parts.append("*(no benchmark-specific key facts extracted; "
                         "see `Other fields` and the .json for raw data.)*")
    else:
        parts.append("*(no extractor for this benchmark; see "
                     "`Other fields` and the .json for raw data.)*")
    parts.append("")
    parts.append("---")
    parts.append("")
    parts.append("## Verifier rule (what the strict verifier checks)")
    parts.append("")
    parts.append(f"> {rule}")
    parts.append("")
    parts.append("This rule is the contract you are auditing in **Q2**.")
    parts.append("")
    parts.append("---")
    parts.append("")
    parts.append("## Policy / instructions (as the model sees them)")
    parts.append("")
    if policy_text:
        parts.append(fmt_quote(str(policy_text)))
    else:
        parts.append("*(no explicit `policy_text`; the operator semantics "
                     "for this task family are described in the paper and "
                     f"in `code/benchmarks/{benchmark}.py`.)*")
    parts.append("")
    parts.append("---")
    parts.append("")
    parts.append("## Other fields (collapsed, for reference)")
    parts.append("")
    if other_fields_md:
        parts.extend(other_fields_md)
    else:
        parts.append("*(everything was already surfaced in Key facts.)*")
    parts.append("")
    parts.append("---")
    parts.append("")
    parts.append("## Audit questions")
    parts.append("")
    parts.append("**Q1 — Naturalness (1–5).** Does this hardened task still "
                 "look like a natural operator problem? See `PROTOCOL.md`.")
    parts.append("")
    parts.append("**Q2 — Verifier validity.** Would the verifier rule above "
                 "accept the same outputs you would accept on this task? "
                 "Choose `agree`, `disagree_too_strict`, `disagree_too_lax`, "
                 "or `disagree_other`.")
    parts.append("")
    parts.append("Append your answer to your responses file under the key "
                 f"`\"{key}\"`. See `responses/EXAMPLE_filled.json`.")
    parts.append("")
    return "\n".join(parts)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Render audit task JSON files into annotator-friendly Markdown."
    )
    parser.add_argument("--tasks-dir", type=Path, default=DEFAULT_TASKS,
                        help="Directory containing manifest.json (default human_audit/tasks).")
    args = parser.parse_args()

    manifest_path = args.tasks_dir / "manifest.json"
    if not manifest_path.exists():
        sys.stderr.write(
            f"[render_tasks] no manifest at {manifest_path}. "
            "Run `python scripts/build_tasks.py` first.\n"
        )
        return 2

    with manifest_path.open(encoding="utf-8") as fh:
        manifest = json.load(fh)

    written = 0
    for entry in manifest["entries"]:
        json_path = KIT_ROOT / entry["json"]
        md_path = KIT_ROOT / entry["md"]
        if not json_path.exists():
            sys.stderr.write(f"[render_tasks] missing {json_path}; skipping.\n")
            continue
        with json_path.open(encoding="utf-8") as fh:
            task_obj = json.load(fh)
        md = render_task_md(entry, task_obj)
        md_path.write_text(md, encoding="utf-8")
        written += 1
    print(f"[render_tasks] wrote {written} markdown task pages under {args.tasks_dir}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
