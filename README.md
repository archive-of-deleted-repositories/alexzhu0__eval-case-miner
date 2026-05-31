# Eval Case Miner

Mine reusable eval cases from AI failure logs.

## Why

Real AI failures often stay in logs instead of becoming repeatable regression fixtures.

This is a baseline HighStar AI developer tool: dependency-light, local-first, and built around one quick command.

## Install

```bash
git clone https://github.com/alexzhu0/eval-case-miner.git
cd eval-case-miner
PYTHONPATH=src python3 -m unittest discover -s tests
```

## Quickstart

```bash
PYTHONPATH=src python3 -m eval_case_miner examples/failures.jsonl --format promptbeat
```

## Examples

Human-readable output:

```bash
PYTHONPATH=src python3 -m eval_case_miner examples/failures.jsonl --format promptbeat
```

Machine-readable output:

```bash
PYTHONPATH=src python3 -m eval_case_miner examples/failures.jsonl --format json
```

## CLI Reference

- `PYTHONPATH=src python3 -m eval_case_miner --help`
- Main demo: `PYTHONPATH=src python3 -m eval_case_miner examples/failures.jsonl --format promptbeat`
- CI gate: `PYTHONPATH=src python3 -m unittest discover -s tests`

## Features

- JSONL failure-log parsing
- Failure status and error detection
- Source line tracking
- Text and JSON output
- Promptbeat-compatible fixture output

## API

The public Python surface is intentionally small:

```python
from eval_case_miner.cli import mine_cases
```

Use the CLI first. Import the Python functions when you want to embed the same behavior in a larger tool.

## Why Star This

It closes the loop from production failures to regression tests.

## Used With

- Feed `--format promptbeat` output directly into `promptbeat-lite`.
- Mine repeated failures from `agent-trace-summarizer` reports when trace failures become regression cases.
- Keep this repo as a supporting utility; the main public story is the eval loop around `promptbeat-lite`.

## Roadmap

See [ROADMAP.md](ROADMAP.md).

## FAQ

**Does this call external AI APIs?**

No. The current release uses the Python standard library only.

**Is this production-ready?**

Treat this as a focused utility. Run it in CI or local review first, then adapt thresholds and examples to your workflow.

**Can I contribute examples?**

Yes. The most useful issue or pull request includes a real input file, expected output, and the workflow where it helps.

## Contributing

Issues and pull requests are welcome when they include a concrete use case or failing example.

Run tests before opening a pull request:

```bash
PYTHONPATH=src python3 -m unittest discover -s tests
```

## License

MIT
