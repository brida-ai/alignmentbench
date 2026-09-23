import json
import tempfile
import unittest
from pathlib import Path

from alignmentbench.io import ValidationError, load_cases, load_predictions


ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "corpora" / "operational-alignment-v0.1.jsonl"


class IoTests(unittest.TestCase):
    def test_public_corpus_validates(self):
        cases = load_cases(CASES)
        self.assertEqual(len(cases), 28)
        self.assertEqual(len({case["id"] for case in cases}), 28)

    def test_prediction_probabilities_must_sum_to_one(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "predictions.jsonl"
            path.write_text(
                json.dumps(
                    {
                        "case_id": "x",
                        "action": "execute",
                        "probabilities": {
                            "execute": 0.7,
                            "review": 0.2,
                            "decline": 0.2,
                        },
                    }
                )
                + "\n",
                encoding="utf-8",
            )
            with self.assertRaises(ValidationError):
                load_predictions(path)


if __name__ == "__main__":
    unittest.main()
