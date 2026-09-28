# Experiment–Evidence Rules

For every experiment that materially supports a paper claim, record the full interpretation chain.

## Required questions
1. What claim is this experiment intended to test?
2. What is compared, under what conditions?
3. Are backbone, data split, training budget, preprocessing, or oracle information comparable?
4. What exact result is reported?
5. What conclusion is directly supported?
6. What stronger conclusion is not supported?
7. What protocol risks remain?

## Evidence strength
Do not reduce paper-internal support merely because external replication is absent.

Direct, well-described experiments with established metrics and relevant baselines may support `strong` or `moderate` paper-internal evidence.

Downgrade when:
- the comparison changes multiple variables at once;
- baselines use materially different backbones/budgets;
- only one dataset supports a broad generalization;
- effect sizes are tiny and uncertainty is not characterized;
- a claimed causal mechanism lacks intervention/ablation evidence;
- only author interpretation, not measured evidence, supports the mechanism.

## Numeric traceability
A claim containing important numeric results should link to evidence that contains the same numbers or to a verified table/figure source. If the linked evidence only gives qualitative context, mark the relation `indirect` and do not present it as the direct numeric source.
