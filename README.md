# Experiment: PREDICTIVE METRIC FOR OPTIMAL BUDGET ALLOCATION IN DIFFERENTIAL PRIVACY

Based on the [original experiment](https://github.com/conseg/TheImpactofDifferentialPrivacyondatautilityinfundamentalmathematicaloperations), but using a real life dataset.

Key difference: sensitivity calculation to satisfy Differential Privacy.

## The Dataset

PNAD Contínua (IBGE - Brasil) - 2026 (primeiro trimestre)

## The Experiment

Objective: evaluate the metric on a t-test equation to compare Northeast and Southeast income (informal vs formal workers)

Steps:

1. Clip and normalize dataset (C = 46_366, the constitutional salary cap, which is set at the salary of Supreme Court justices). Must be a value taken from the real world, not from the dataset.
2. Calculate necessary statistics and their sensitivities
3. For each possible budget allocation with total epsilon=12, granularity=0.5, epsilon > 0 (1,352,078 possibilities): evaluate the metric for the statistics and the budget allocation sequence
4. Save all possible scores and budget allocation sequences to csv for further analysis, and print the best metric score.

## Estimated Experiment Execution Time

To reproduce (in a Linux shell):

1. `time python ./experiment.py real`
2. Send an interrupt (Ctrl+C) when N exceeds 500.
3. To find the number of hours, based on the last N and the elapsed time (t): `((1352078*t)/n)/3600`

Tested Hardware:

- Laptop (Intel Core i5 1135G7 - 8GB RAM)
- Desktop (AMD Ryzen 7 8700G - 32GB RAM)

Partial Results:

- Laptop: 514 iterations in 12.13s
- Desktop: 493 iterations in 8.11s

Total Results:

- Estimated total time on the Laptop: 8h51m
- Estimated total time on the Desktop: 6h10m

## Tasks

1. Provide a way to run the experiment in parts, to allow parallel execution on multiple CPUs.
2. Run the experiment to evaluate the metric.
3. Combine the resulting CSVs into one.
4. Analyze the csv to find notable metric scores for specific sequences.
