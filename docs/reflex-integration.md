# Reflex Alignment integration

AlignmentBench integrates with the public **Reflex Alignment** use case:

https://github.com/brida-ai/reflex/tree/main/examples/use-cases/alignment

## Separation of roles

The benchmark keeps three concepts separate:

1. **case policy** — explicit principles and deterministic checks;
2. **benchmark truth** — frozen acceptable actions and preferred action;
3. **Reflex audit** — an independent semantic classification of one proposed action.

Reflex does not overwrite benchmark truth.

## Generate audit states

```bash
python3 -m alignmentbench.cli reflex-states \
  --cases corpora/operational-alignment-v0.1.jsonl \
  --predictions predictions.jsonl \
  --output reflex-states.jsonl
```

Each row contains:

- `case_id`;
- canonical Reflex id/version;
- bounded `state`;
- target model's selected action;
- expected Reflex branch for that action.

## Execute with the Brida SDK

Install the official SDK:

```bash
pnpm add @brida/sdk
```

Then run the generated states with a server-side API key:

```js
import { Brida } from '@brida/sdk'

const brida = new Brida({ apiKey: process.env.BRIDA_API_KEY })

const result = await brida.reflex.run('alignment', {
  state: row.state,
})

console.log(result.decision.branch)
```

Use only a released hosted Reflex version and record its exact identity in the evaluation receipt.

## Evaluator independence

Do not evaluate a target model with the exact same model/checkpoint acting as its sole judge.

For serious comparisons record:

- target model/checkpoint;
- Reflex recipe version;
- Reflex decision-engine/model revision;
- sampling/inference configuration;
- corpus hash.

If the semantic judge disagrees with frozen benchmark truth, report the disagreement. Do not silently relabel the benchmark case.

## Runtime use

The same Reflex can also sit in front of real agent actions:

```text
agent
 -> proposed action
 -> Reflex Alignment
 -> deterministic host policy
 -> execute / review / block
```

That runtime pattern is complementary to AlignmentBench. The benchmark measures behavior; Reflex Alignment supervises execution.
