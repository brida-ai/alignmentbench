# Versioning

AlignmentBench versions the **benchmark definition**, not model performance.

## Developer Preview

`v0.x` releases may refine task wording, schemas and methodology. Every public receipt must record the exact benchmark version and corpus hash.

## Stable benchmark

`v1.0.0` will freeze the first stable public benchmark definition.

After v1:

- new model or checkpoint results on an unchanged benchmark may be added without changing the benchmark major version;
- changes to cases, gold labels, acceptable actions or scoring that alter comparability require a new benchmark version;
- editorial documentation fixes that do not affect evaluation semantics may remain within the same benchmark line.

Never compare receipts as if they were directly equivalent when their benchmark version or corpus hash differs.
