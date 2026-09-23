# Training-time checkpoint evaluation

AlignmentBench can be used while a model is being trained or post-trained, but the safest interpretation is **regression monitoring**, not "the benchmark trains alignment."

## Recommended loop

```text
checkpoint N
  -> frozen prompt adapter
  -> public development suite
  -> private rotating holdout
  -> predictions + probabilities
  -> deterministic AlignmentBench receipt
  -> optional independent Reflex Alignment audit
  -> compare with checkpoint N-1
  -> investigate regressions before continuing
```

## What to gate on

Do not gate a training run on one global number. Useful gates include:

- zero new critical policy violations;
- no material regression in authority-boundary compliance;
- no material regression in interruptibility/oversight;
- unsafe-execution rate below an agreed threshold;
- stable or improving appropriate-escalation behavior;
- explicit review of any dimension that regresses beyond tolerance.

## Public vs private cases

The public suite should be treated as a development set. If a training team repeatedly sees every exact case, benchmark optimization becomes increasingly likely.

For release decisions, add:

- private holdouts;
- paraphrase and option-order variants;
- novel policies;
- longer trajectories;
- adversarial framing;
- cases generated after the checkpoint was trained.

Store private cases outside this public repository.

## Checkpoint identity

Every receipt should record enough information to recover the tested artifact:

- model family;
- exact checkpoint/revision;
- tokenizer or interface revision when relevant;
- sampling settings;
- adapter version;
- benchmark corpus hash;
- evaluator identity if Reflex or another model judge is used.

## Avoiding reward hacking

Using a frozen public benchmark directly as the only training reward is discouraged. A model can improve on a known exam without acquiring the general behavior the exam is meant to measure.

Prefer using AlignmentBench to:

1. detect regressions;
2. diagnose failure modes;
3. create new training data from classes of failures;
4. evaluate again on fresh holdouts.
