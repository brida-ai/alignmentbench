# Contributing

AlignmentBench is an open benchmark. Contributions are welcome when they preserve reproducibility and the benchmark's narrow scope.

## Case contributions

Public cases must:

- be synthetic or fully public;
- contain no customer data, credentials or private Brida material;
- avoid actionable harmful instructions;
- state explicit policy rather than rely on hidden evaluator assumptions;
- define policy-compliant actions, a preferred action and Reflex branch expectations;
- identify the behavioral dimension and severity.

Changes to the frozen corpus that alter comparability require a benchmark version change.

## Code

Run before opening a pull request:

```bash
python3 tools/build_public_corpus.py
python3 -m unittest discover -s tests -p 'test_*.py' -v
python3 -m alignmentbench.cli validate --cases corpora/operational-alignment-v0.1.jsonl
```

Do not include API keys, provider credentials, private holdouts or unpublished model data.
