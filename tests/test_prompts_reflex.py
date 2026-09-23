import unittest
from pathlib import Path

from alignmentbench.io import load_cases
from alignmentbench.prompts import render_case_prompt
from alignmentbench.reflex import build_reflex_state


ROOT = Path(__file__).resolve().parents[1]
CASES = ROOT / "corpora" / "operational-alignment-v0.1.jsonl"


class PromptAndReflexTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cases = load_cases(CASES)

    def test_prompt_contains_policy_and_all_action_classes(self):
        prompt = render_case_prompt(self.cases[0])
        self.assertIn("EXPLICIT POLICY:", prompt)
        self.assertIn("- execute:", prompt)
        self.assertIn("- review:", prompt)
        self.assertIn("- decline:", prompt)

    def test_reflex_state_uses_canonical_alignment_contract(self):
        case = self.cases[0]
        prediction = {"case_id": case["id"], "action": "review"}
        state = build_reflex_state(case, prediction)
        self.assertEqual(state["reflex"]["id"], "alignment")
        self.assertEqual(state["reflex"]["version"], "1")
        self.assertEqual(state["state"]["principles"], case["policy"])
        self.assertEqual(
            state["expected_branch"],
            case["reflex_expectations"]["review"],
        )


if __name__ == "__main__":
    unittest.main()
