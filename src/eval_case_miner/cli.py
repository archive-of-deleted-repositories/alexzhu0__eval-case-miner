"""Mine reusable eval cases from AI failure logs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List, Sequence


FAILURE_STATUSES = {"fail", "failed", "failure", "error", "timeout", "rejected"}


def load_jsonl(path: str) -> List[Dict[str, Any]]:
    rows = []
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        if line.strip():
            payload = json.loads(line)
            if isinstance(payload, dict):
                rows.append(payload)
    return rows


def mine_cases(path: str) -> List[Dict[str, Any]]:
    cases = []
    for index, row in enumerate(load_jsonl(path), start=1):
        status = str(row.get("status") or row.get("outcome") or "").lower()
        if status not in FAILURE_STATUSES and not row.get("error"):
            continue
        prompt = str(row.get("prompt") or row.get("input") or row.get("question") or "").strip()
        expected = str(row.get("expected") or row.get("expected_output") or row.get("should") or "").strip()
        actual = str(row.get("actual") or row.get("output") or row.get("response") or "").strip()
        reason = str(row.get("error") or row.get("reason") or status or "failure").strip()
        cases.append(
            {
                "id": row.get("id") or f"case-{index}",
                "prompt": prompt,
                "expected": expected or "Define the expected safe/correct behavior.",
                "actual": actual,
                "reason": reason,
                "tags": row.get("tags") or ["mined-failure"],
            }
        )
    return cases


def format_text(cases: List[Dict[str, Any]]) -> str:
    lines = [f"Mined eval cases: {len(cases)}", ""]
    for case in cases:
        lines.extend(
            [
                f"## {case['id']}",
                f"Reason: {case['reason']}",
                f"Prompt: {case['prompt']}",
                f"Expected: {case['expected']}",
                f"Actual: {case['actual']}",
                "",
            ]
        )
    return "\n".join(lines).rstrip()


def run(input_path: str, output_format: str = "text") -> str:
    cases = mine_cases(input_path)
    if output_format == "json":
        return json.dumps({"cases": cases}, indent=2, sort_keys=True)
    return format_text(cases)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Mine reusable eval cases from AI failure logs.")
    parser.add_argument("input", help="JSONL failure log")
    parser.add_argument("--format", choices=["text", "json"], default="text")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    print(run(args.input, args.format))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
