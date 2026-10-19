import json
import tempfile
import unittest
from pathlib import Path

from token_policy import validated, resolved_agent_model
from token_report import summarize

class PolicyTests(unittest.TestCase):
    def test_v591_backwards_compatibility(self):
        policy = validated(None)
        self.assertEqual(resolved_agent_model("planner", policy), "opus")
        self.assertEqual(resolved_agent_model("java-developer", policy), "inherit")
        self.assertFalse(policy["auxiliary_enabled"])

    def test_no_auxiliary_without_approval(self):
        with self.assertRaises(ValueError):
            validated({"auxiliary_enabled": True, "auxiliary_model": "haiku"})

    def test_auxiliary_opt_in(self):
        p = validated({"auxiliary_enabled": True, "user_approved": True,
                       "auxiliary_model": "haiku"})
        self.assertEqual(resolved_agent_model("log-summarizer", p), "haiku")
        self.assertEqual(resolved_agent_model("security-reviewer", p), "inherit")

    def test_invalid_role_model(self):
        with self.assertRaises(ValueError):
            validated({"planning_model": "unverified-model"})

    def test_token_report_deduplicates_message_ids(self):
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / "session.jsonl"
            record = {"message": {"role": "assistant", "id": "m1", "model": "test",
                                   "usage": {"input_tokens": 10, "output_tokens": 5,
                                             "cache_read_input_tokens": 20}}}
            path.write_text(json.dumps(record) + "\n" + json.dumps(record) + "\n")
            result = summarize([path])
            self.assertEqual(result["totals"]["calls"], 1)
            self.assertEqual(result["totals"]["cache_read_input_tokens"], 20)

if __name__ == "__main__":
    unittest.main()
