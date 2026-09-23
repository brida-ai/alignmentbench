from __future__ import annotations

from typing import Any


REFLEX_ID = "alignment"
REFLEX_VERSION = "1"
REFLEX_RECIPE_URL = (
    "https://github.com/brida-ai/reflex/tree/main/examples/use-cases/alignment"
)


def build_reflex_state(case: dict[str, Any], prediction: dict[str, Any]) -> dict[str, Any]:
    action_id = prediction["action"]
    return {
        "case_id": case["id"],
        "reflex": {
            "id": REFLEX_ID,
            "version": REFLEX_VERSION,
            "source": REFLEX_RECIPE_URL,
        },
        "state": {
            "action": case["actions"][action_id],
            "purpose": case["purpose"],
            "effect": case["effect"],
            "reversible": case["reversible"],
            "principles": case["policy"],
            "deterministicChecks": case["deterministic_checks"],
        },
        "selected_action": action_id,
        "expected_branch": case["reflex_expectations"][action_id],
    }
