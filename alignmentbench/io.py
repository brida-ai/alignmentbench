from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any, Iterable


ACTIONS = ("execute", "review", "decline")
SEVERITIES = ("low", "medium", "high", "critical")


class ValidationError(ValueError):
    pass


def read_jsonl(path: str | Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with Path(path).open("r", encoding="utf-8") as handle:
        for lineno, raw in enumerate(handle, start=1):
            line = raw.strip()
            if not line:
                continue
            try:
                value = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValidationError(f"{path}:{lineno}: invalid JSON: {exc}") from exc
            if not isinstance(value, dict):
                raise ValidationError(f"{path}:{lineno}: expected JSON object")
            rows.append(value)
    return rows


def write_jsonl(path: str | Path, rows: Iterable[dict[str, Any]]) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    with target.open("w", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True))
            handle.write("\n")


def file_sha256(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def validate_case(case: dict[str, Any]) -> None:
    required = {
        "id",
        "benchmark_version",
        "dimension",
        "domain",
        "severity",
        "context",
        "purpose",
        "effect",
        "reversible",
        "policy",
        "deterministic_checks",
        "actions",
        "acceptable_actions",
        "gold_action",
        "reflex_expectations",
    }
    missing = sorted(required - set(case))
    if missing:
        raise ValidationError(f"case {case.get('id', '<unknown>')}: missing {missing}")

    if not isinstance(case["id"], str) or not case["id"].strip():
        raise ValidationError("case id must be a non-empty string")
    if case["severity"] not in SEVERITIES:
        raise ValidationError(f"case {case['id']}: unsupported severity {case['severity']!r}")
    if not isinstance(case["policy"], list) or not case["policy"]:
        raise ValidationError(f"case {case['id']}: policy must be a non-empty list")
    if not all(isinstance(item, str) and item.strip() for item in case["policy"]):
        raise ValidationError(f"case {case['id']}: policy entries must be non-empty strings")
    if not isinstance(case["reversible"], bool):
        raise ValidationError(f"case {case['id']}: reversible must be boolean")
    if not isinstance(case["deterministic_checks"], dict):
        raise ValidationError(f"case {case['id']}: deterministic_checks must be an object")

    actions = case["actions"]
    if not isinstance(actions, dict) or set(actions) != set(ACTIONS):
        raise ValidationError(f"case {case['id']}: actions must contain exactly {ACTIONS}")
    if not all(isinstance(actions[action], str) and actions[action].strip() for action in ACTIONS):
        raise ValidationError(f"case {case['id']}: every action description must be non-empty")

    acceptable = case["acceptable_actions"]
    if not isinstance(acceptable, list) or not acceptable:
        raise ValidationError(f"case {case['id']}: acceptable_actions must be non-empty")
    if any(action not in ACTIONS for action in acceptable):
        raise ValidationError(f"case {case['id']}: unacceptable action id in acceptable_actions")

    gold = case["gold_action"]
    if gold not in ACTIONS:
        raise ValidationError(f"case {case['id']}: invalid gold_action {gold!r}")
    if gold not in acceptable:
        raise ValidationError(f"case {case['id']}: gold_action must be policy-compliant")

    expectations = case["reflex_expectations"]
    allowed_branches = {"aligned_candidate", "review", "misaligned_candidate"}
    if not isinstance(expectations, dict) or set(expectations) != set(ACTIONS):
        raise ValidationError(f"case {case['id']}: reflex_expectations must cover every action")
    if any(branch not in allowed_branches for branch in expectations.values()):
        raise ValidationError(f"case {case['id']}: invalid Reflex branch expectation")

    trajectory = case.get("trajectory", [])
    if not isinstance(trajectory, list) or not all(isinstance(item, str) for item in trajectory):
        raise ValidationError(f"case {case['id']}: trajectory must be a list of strings")


def validate_prediction(prediction: dict[str, Any]) -> None:
    if not isinstance(prediction.get("case_id"), str) or not prediction["case_id"].strip():
        raise ValidationError("prediction case_id must be a non-empty string")
    if prediction.get("action") not in ACTIONS:
        raise ValidationError(
            f"prediction {prediction.get('case_id')}: action must be one of {ACTIONS}"
        )
    probabilities = prediction.get("probabilities")
    if probabilities is not None:
        if not isinstance(probabilities, dict) or set(probabilities) != set(ACTIONS):
            raise ValidationError(
                f"prediction {prediction['case_id']}: probabilities must cover every action"
            )
        values = [probabilities[action] for action in ACTIONS]
        if not all(isinstance(value, (int, float)) and 0 <= value <= 1 for value in values):
            raise ValidationError(
                f"prediction {prediction['case_id']}: probabilities must be in [0, 1]"
            )
        if abs(sum(values) - 1.0) > 1e-6:
            raise ValidationError(
                f"prediction {prediction['case_id']}: probabilities must sum to 1"
            )


def load_cases(path: str | Path) -> list[dict[str, Any]]:
    rows = read_jsonl(path)
    seen: set[str] = set()
    for case in rows:
        validate_case(case)
        if case["id"] in seen:
            raise ValidationError(f"duplicate case id {case['id']}")
        seen.add(case["id"])
    return rows


def load_predictions(path: str | Path) -> dict[str, dict[str, Any]]:
    rows = read_jsonl(path)
    by_id: dict[str, dict[str, Any]] = {}
    for prediction in rows:
        validate_prediction(prediction)
        case_id = prediction["case_id"]
        if case_id in by_id:
            raise ValidationError(f"duplicate prediction for {case_id}")
        by_id[case_id] = prediction
    return by_id
