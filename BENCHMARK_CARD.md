# AlignmentBench v0.1 benchmark card

## Name

AlignmentBench

## Version

0.1.0 — Developer Preview

## Maintainer

Brida

## Purpose

Measure whether an AI system's operational action choices remain consistent with explicit policies and authority boundaries.

## Intended uses

- checkpoint regression testing during model training or post-training;
- pre-deployment behavioral evaluation of tool-using agents;
- evaluation of operational policy adherence;
- research on semantic supervision and escalation behavior;
- validation of Reflex Alignment as an independent semantic audit layer.

## Out-of-scope claims

A high result does not demonstrate:

- general or moral alignment;
- safe internal objectives;
- absence of deception outside tested scenarios;
- political or ideological neutrality;
- safety under arbitrary capabilities or access;
- certification for any regulated or safety-critical deployment.

## Dataset

Brida-authored synthetic scenarios only.

The public v0.1 suite contains abstract operational situations across software, data, business workflows, healthcare-like administrative workflows and simulated high-impact infrastructure contexts. It intentionally contains no real customer data and no actionable instructions for harmful operation of critical systems.

## Outputs

AlignmentBench reports a profile, not one global score:

- completion;
- policy compliance;
- best-action accuracy;
- unsafe execution;
- appropriate escalation;
- over-caution;
- critical policy violations;
- per-dimension results;
- optional NLL/Brier;
- critical failure IDs.

## Known limitations

- small public suite;
- synthetic wording;
- public cases can be memorized or optimized directly;
- three action classes simplify real-world action spaces;
- gold policy interpretation is authored by benchmark maintainers;
- open-ended semantic scoring can inherit evaluator bias;
- high-impact domains are deliberately abstract rather than realistic operational replicas.

## Recommended use

Pair the public suite with private, rotating, adversarial and trajectory-based holdouts. Record target model/checkpoint identity and any evaluator identity in every result receipt.
