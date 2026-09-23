import unittest
from pathlib import Path

from alignmentbench.io import load_cases
from alignmentbench.scoring import score


ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "corpora" / "operational-alignment-v0.1.jsonl"


class ScoringTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases = load_cases(CASES)

    def test_gold_predictions_are_perfect(self):
        predictions = {
            case["id"]: {
                "case_id": case["id"],
                "action": case["gold_action"],
                "probabilities": {
                    action: 1.0 if action == case["gold_action"] else 0.0
                    for action in ("execute", "review", "decline")
                },
            }
            for case in self.cases
        }
        report = score(self.cases, predictions)
        self.assertEqual(report["completion_rate"], 1.0)
        self.assertEqual(report["policy_compliance_rate"], 1.0)
        self.assertEqual(report["best_action_accuracy"], 1.0)
        self.assertEqual(report["critical_policy_violation_rate"], 0.0)
        self.assertEqual(report["unsafe_execution_count"], 0)
        self.assertEqual(report["gold_action_nll"], 0.0)
        self.assertEqual(report["multiclass_brier"], 0.0)

    def test_missing_predictions_are_retained_as_failures(self):
        report = score(self.cases, {})
        self.assertEqual(report["completion_rate"], 0.0)
        self.assertEqual(report["policy_compliance_rate"], 0.0)
        self.assertEqual(report["best_action_accuracy"], 0.0)
        self.assertEqual(len(report["missing_prediction_ids"]), 28)

    def test_execute_everything_surfaces_critical_failures(self):
        predictions = {
            case["id"]: {"case_id": case["id"], "action": "execute"}
            for case in self.cases
        }
        report = score(self.cases, predictions)
        self.assertGreater(report["unsafe_execution_count"], 0)
        self.assertGreater(report["critical_policy_violation_count"], 0)
        self.assertGreater(len(report["critical_failure_ids"]), 0)
        self.assertLess(report["policy_compliance_rate"], 1.0)


if __name__ == "__main__":
    unittest.main()
