from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from . import __version__
from .io import load_cases, load_predictions, write_jsonl
from .prompts import render_case_prompt
from .receipt import build_receipt
from .reflex import build_reflex_state
from .scoring import score


def _write_json(path: str, value: dict[str, Any]) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def command_validate(args: argparse.Namespace) -> int:
    cases = load_cases(args.cases)
    print(f"ok: {len(cases)} cases")
    return 0


def command_prompts(args: argparse.Namespace) -> int:
    cases = load_cases(args.cases)
    rows = [
        {
            "case_id": case["id"],
            "benchmark_version": case["benchmark_version"],
            "prompt": render_case_prompt(case),
        }
        for case in cases
    ]
    write_jsonl(args.output, rows)
    print(f"wrote {len(rows)} prompts to {args.output}")
    return 0


def command_score(args: argparse.Namespace) -> int:
    cases = load_cases(args.cases)
    predictions = load_predictions(args.predictions)
    metrics = score(cases, predictions)
    benchmark_version = str(cases[0]["benchmark_version"]) if cases else __version__
    receipt = build_receipt(
        benchmark_version=benchmark_version,
        cases_path=args.cases,
        predictions_path=args.predictions,
        report=metrics,
        target=args.target,
        checkpoint=args.checkpoint,
    )
    _write_json(args.output, receipt)
    print(json.dumps(metrics, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


def command_reflex_states(args: argparse.Namespace) -> int:
    cases = load_cases(args.cases)
    predictions = load_predictions(args.predictions)
    rows: list[dict[str, Any]] = []
    for case in cases:
        prediction = predictions.get(case["id"])
        if prediction is None:
            continue
        rows.append(build_reflex_state(case, prediction))
    write_jsonl(args.output, rows)
    print(f"wrote {len(rows)} Reflex states to {args.output}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="alignmentbench",
        description="AlignmentBench operational alignment evaluation harness",
    )
    parser.add_argument("--version", action="version", version=__version__)
    sub = parser.add_subparsers(dest="command", required=True)

    validate = sub.add_parser("validate", help="validate a frozen case corpus")
    validate.add_argument("--cases", required=True)
    validate.set_defaults(func=command_validate)

    prompts = sub.add_parser("prompts", help="render benchmark prompts")
    prompts.add_argument("--cases", required=True)
    prompts.add_argument("--output", required=True)
    prompts.set_defaults(func=command_prompts)

    score_parser = sub.add_parser("score", help="score model predictions")
    score_parser.add_argument("--cases", required=True)
    score_parser.add_argument("--predictions", required=True)
    score_parser.add_argument("--output", required=True)
    score_parser.add_argument("--target")
    score_parser.add_argument("--checkpoint")
    score_parser.set_defaults(func=command_score)

    reflex_states = sub.add_parser(
        "reflex-states", help="emit Reflex Alignment states for predictions"
    )
    reflex_states.add_argument("--cases", required=True)
    reflex_states.add_argument("--predictions", required=True)
    reflex_states.add_argument("--output", required=True)
    reflex_states.set_defaults(func=command_reflex_states)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main())
