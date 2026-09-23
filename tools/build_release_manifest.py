from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VERSION = "0.1.0"
FILES = [
    "README.md",
    "METHODOLOGY.md",
    "BENCHMARK_CARD.md",
    "VERSIONING.md",
    "corpora/operational-alignment-v0.1.jsonl",
    "configs/reflex-alignment-v1.json",
]


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    digest.update(path.read_bytes())
    return digest.hexdigest()


def main() -> None:
    manifest = {
        "schema": "brida.ai/alignmentbench/release-manifest/v0.1",
        "benchmark_version": VERSION,
        "files": [
            {
                "path": rel,
                "sha256": sha256(ROOT / rel),
                "bytes": (ROOT / rel).stat().st_size,
            }
            for rel in FILES
        ],
    }
    target = ROOT / "release" / "v0.1-manifest.json"
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    print(target.relative_to(ROOT))


if __name__ == "__main__":
    main()
