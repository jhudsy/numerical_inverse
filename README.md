# Inverse Gradual Semantics Solver

This code solves the inverse problem numerically for the following gradual semantics:

- h-categorizer
- max based semantics
- cardinality (card) semantics

It was designed to run on a HPC cluster. `sbatch_generator.py` prepares a set of `.job` files for running, which are run via `sbatchrun.sh`. The `datawrangle.py` script then combines all the different CSVs into a single CSV. 

Our results can be found in `data.csv`.
