# AlignmentBench

**Open behavioral benchmark for operational alignment under explicit policies.**

AlignmentBench evaluates whether an AI system chooses actions that remain inside explicit authority, policy, uncertainty, impact and oversight boundaries.

It is designed for two moments:

1. **checkpoint evaluation** — run the same frozen suite while a model is being trained or post-trained and detect behavioral regressions;
2. **agent evaluation** — test proposed actions and trajectories before deployment in systems that can use tools or create side effects.

AlignmentBench is not a universal measurement of whether a model is "aligned with humanity." It measures a narrower, testable question: **does the system behave consistently with the explicit operational constraints supplied to it?**

> **Developer Preview v0.1.0.** The public suite is intentionally small and synthetic. Treat it as a reproducible development benchmark, not a certification.

## Why another benchmark?

There are already strong projects for alignment auditing, hidden-behavior discovery and automated behavioral evaluation. AlignmentBench has a different scope: **operational alignment under an explicit policy at the point where a model chooses what to do.**

The core loop is:

```text
model / checkpoint
  -> bounded scenario + explicit policy
  -> proposed operational action
  -> deterministic benchmark scoring
  -> optional Reflex Alignment semantic audit
  -> alignment profile + regression receipt
```

The public benchmark does **not** collapse everything into one "alignment score." It reports separate dimensions and failure modes so an improvement in one area cannot hide a regression in another.

## v0.1 dimensions

The first suite covers seven dimensions:

- **authority boundary** — does the system stay inside granted authority?
- **instruction conflict** — does it resolve conflicting instructions using the supplied policy?
- **uncertainty and escalation** — does it ask for review when evidence is insufficient?
- **reversibility and impact** — does higher-impact or irreversible action receive the required gate?
- **scope integrity** — does the system avoid expanding its objective beyond the requested task?
- **interruptibility and oversight** — does it respect pause, stop and human-approval requirements?
- **trajectory integrity** — does a multi-step history change the next action when the policy says it should?

All included scenarios are synthetic. High-impact domains are represented abstractly; the corpus contains no operational instructions for weapons, critical infrastructure exploitation or other dangerous activity.

## Action contract

Every public case asks the target system to choose one of three operational classes:

- `execute` — perform the bounded action now;
- `review` — escalate for human or higher-authority review;
- `decline` — do not perform the requested action.

A case can have more than one policy-compliant action, while still identifying one `gold_action` as the best operational response. That lets the benchmark separate **policy compliance** from **best-action accuracy**.

## Metrics

AlignmentBench v0.1 reports:

- completion rate;
- policy-compliance rate;
- best-action accuracy;
- unsafe-execution rate;
- appropriate-escalation rate;
- over-caution rate;
- critical-policy-violation rate;
- per-dimension compliance and best-action accuracy;
- critical failure IDs;
- optional probability NLL and multiclass Brier score.

These are reported separately. There is deliberately no single global "aligned / not aligned" score.

## Quick start

Requires Python 3.11+ and has no runtime dependencies.

```bash
python -m unittest discover -s tests -p 'test_*.py' -v

python -m alignmentbench.cli validate \
  --cases corpora/operational-alignment-v0.1.jsonl

python -m alignmentbench.cli prompts \
  --cases corpora/operational-alignment-v0.1.jsonl \
  --output /tmp/alignmentbench-prompts.jsonl

python -m alignmentbench.cli score \
  --cases corpora/operational-alignment-v0.1.jsonl \
  --predictions examples/sample-predictions.jsonl \
  --output results/sample/receipt.json
```

## Training-time checkpoint loop

A training pipeline can run AlignmentBench on every selected checkpoint:

```text
checkpoint N
 -> benchmark adapter
 -> public development suite
 -> private rotating holdout (recommended)
 -> deterministic receipt
 -> compare with checkpoint N-1
 -> investigate regressions
```

The public corpus is useful for development and reproducibility. For serious training or release gates, use additional **private, rotating and adversarial holdouts** so the model cannot simply learn the public exam.

See [docs/checkpoint-evaluation.md](docs/checkpoint-evaluation.md).

## Brida Reflex integration

AlignmentBench works with the public [Reflex Alignment](https://github.com/brida-ai/reflex/tree/main/examples/use-cases/alignment) contract.

The benchmark keeps two roles separate:

- **ground truth / benchmark scoring:** frozen case labels and policy-compliant action sets;
- **semantic audit:** Reflex Alignment can independently classify the model's proposed action as `aligned_candidate`, `review` or `misaligned_candidate`.

Reflex is therefore an evaluator and runtime supervision layer, not the source of benchmark truth.

Generate Reflex-ready states from a model run:

```bash
python -m alignmentbench.cli reflex-states \
  --cases corpora/operational-alignment-v0.1.jsonl \
  --predictions examples/sample-predictions.jsonl \
  --output /tmp/reflex-states.jsonl
```

See [docs/reflex-integration.md](docs/reflex-integration.md) for the SDK execution example and evaluator-identity requirements.

## Benchmark hygiene

For comparable results:

- freeze corpus and benchmark version;
- record model/checkpoint identity;
- record evaluator identity when an LLM/Reflex judge is used;
- never silently delete provider failures or missing rows;
- separate public development sets from private release holdouts;
- report each dimension and critical failure independently;
- evaluate trajectories, not only final prose, for agentic systems.

## Repository layout

- `alignmentbench/` — validation, prompting, scoring and receipt logic;
- `corpora/` — frozen Brida-authored synthetic public suite;
- `configs/` — integration contracts and frozen evaluator references;
- `docs/` — methodology and checkpoint/Reflex guidance;
- `examples/` — sample predictions and Reflex runner;
- `tests/` — reproducibility and scoring tests;
- `results/` — example machine-readable receipts.

## Relationship to ReflexBench

[ReflexBench](https://github.com/brida-ai/reflexbench) evaluates **decision engines**: semantic quality, calibration, multilingual consistency, robustness and typed decision behavior.

AlignmentBench evaluates **target-system behavior under explicit operational policy**.

They are complementary:

```text
ReflexBench    -> how good is the decision engine?
AlignmentBench -> how well does the target system stay within operational constraints?
Reflex Alignment -> semantic supervision at execution time
```

## License

Apache-2.0 for Brida-authored code, documentation and synthetic fixtures.
