import json
import tempfile
import unittest
from pathlib import Path

from eval_case_miner.cli import mine_cases, run


class EvalCaseMinerTests(unittest.TestCase):
    def test_mines_failed_rows(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "failures.jsonl"
            path.write_text(
                json.dumps({"id": "a", "status": "failed", "prompt": "hi", "actual": "bad"}) + "\n"
                + json.dumps({"id": "b", "status": "ok", "prompt": "fine"}) + "\n",
                encoding="utf-8",
            )
            cases = mine_cases(str(path))
        self.assertEqual(len(cases), 1)
        self.assertEqual(cases[0]["id"], "a")

    def test_json_output_contains_cases(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "failures.jsonl"
            path.write_text('{"status":"error","input":"x","error":"timeout"}\n', encoding="utf-8")
            payload = json.loads(run(str(path), "json"))
        self.assertEqual(payload["cases"][0]["reason"], "timeout")


if __name__ == "__main__":
    unittest.main()
