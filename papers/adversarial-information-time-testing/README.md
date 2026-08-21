# Adversarial Information-Time Testing for Financial Machine-Learning Pipelines

**A Mutation-Based Benchmark for Temporal Leakage Detection**

Edmen Wong · Alpha Tick Lab Research / AQP TECH ENTERPRISE

Research Paper 01 · Public Preprint · Version 0.2 · 22 August 2026

Canonical page: https://alphaquantpro.com/research/adversarial-information-time-testing

DOI: https://doi.org/10.5281/zenodo.22049285

This repository directory contains the reference benchmark and publication artifacts for the paper. The paper extends the information-time contract introduced in Technical Note 01 and focuses on mutation-based falsification, paired causal/leaky fixtures, benchmark evidence, and mutation adequacy.

## Main result

- Six causal controls × 600 trials each: **0 / 3,600 violations**.
- Five targeted leaky fixture classes × 600 trials each: **3,000 / 3,000 detected**.
- Same-open retro-execution with a random unavailable-close mutation: **286 / 600 detected**.
- The same planted execution fault with a targeted sign-flip adversary: **600 / 600 detected**.

The execution contrast is intentional: finite mutation testing is only as strong as the mutation family used to excite a dependency. Passing one weak mutation is not proof of causal correctness.

## Reproduce

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements-reference.txt
python aitt_benchmark.py --seeds 200 --out results
```

Reference environment:

- Python 3.13.5
- NumPy 2.3.5
- pandas 2.2.3
- SciPy 1.17.0
- scikit-learn 1.8.0

## Files

- `aitt_benchmark.py` - synthetic generator, paired fixtures, mutation operators, and reporting.
- `results/reference-summary.csv` - reference summary used by the public preprint.
- `paper-v0.2.pdf` - public manuscript.
- `citation.bib` - BibTeX citation metadata.

## Evidence boundary

This is a controlled fault-injection benchmark. It does not estimate the prevalence of leakage in real production systems, prove that a pipeline is universally causal, or establish predictive skill, strategy profitability, transaction-cost realism, capacity, or live-trading performance.

## Verification note

The publication reference run was generated with Python 3.13.5. Before this public release, the same benchmark was rerun on Windows with Python 3.11.15 using the pinned package versions above. The reported fixture counts, violation rates, and median maximum deviations reproduced exactly, including the 286/600 random execution result and 600/600 targeted execution result.
