from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from .io import file_sha256


def build_receipt(
    *,
    benchmark_version: str,
    cases_path: str,
    predictions_path: str,
    report: dict[str, Any],
    target: str | None,
    checkpoint: str | None,
) -> dict[str, Any]:
    return {
        "schema": "brida.ai/alignmentbench/receipt/v0.1",
        "benchmark_version": benchmark_version,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "target": {
            "name": target,
            "checkpoint": checkpoint,
        },
        "inputs": {
            "cases_path": cases_path,
            "cases_sha256": file_sha256(cases_path),
            "predictions_path": predictions_path,
            "predictions_sha256": file_sha256(predictions_path),
        },
        "metrics": report,
    }
