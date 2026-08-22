# Alpha Quant Pro Lab Research

Public research papers, technical notes, and reproducibility artifacts from **Alpha Quant Pro Lab**, published by **AQP TECH ENTERPRISE**.

The program focuses on quantitative research methodology, information-time causality, temporal leakage, financial machine learning, walk-forward validation, execution realism, and reproducible research-to-runtime workflows.

## Research Paper 01

### Adversarial Information-Time Testing for Financial Machine-Learning Pipelines

**A Mutation-Based Benchmark for Temporal Leakage Detection**

- Author: **Edmen Wong**
- Affiliation: **Alpha Quant Pro Lab Research · AQP TECH ENTERPRISE**
- Status: **Public preprint; not peer reviewed**
- Version: **0.3**
- Published: **22 August 2026**
- Latest version DOI: **10.5281/zenodo.22052205**
- Concept DOI: **10.5281/zenodo.22049284**
- Archive: https://doi.org/10.5281/zenodo.22052205
- Canonical page: https://alphaquantpro.com/research/adversarial-information-time-testing
- Reproducibility: `papers/adversarial-information-time-testing/`

The paper formalizes authorization-preserving mutations and artifact-level temporal invariance tests across feature engineering, preprocessing, selection, label maturity, completed-bar availability, and execution authority.

Controlled benchmark result: 0/3,600 violations in causal controls; 3,000/3,000 detections across five targeted leakage classes; and an execution experiment showing that random mutation detects only 286/600 planted faults while a targeted adversary detects 600/600.

## Technical Note 01

### Bar Time Is Not Information Time

**A Causality Contract for Quantitative Trading Pipelines**

- Author: **Edmen Wong**
- Version: **1.1**
- Latest revision: **22 August 2026**
- First published: **16 August 2026**
- Latest version DOI: **10.5281/zenodo.22052190**
- Concept DOI: **10.5281/zenodo.21965787**
- Canonical page: https://alphaquantpro.com/research/bar-time-is-not-information-time
- Archive: https://doi.org/10.5281/zenodo.22052190

The note introduces an explicit information-time contract separating storage timestamps from information availability, label maturity, fold-local research state, and executable signal timing.

## Research progression

```text
Technical Note 01
  information-time contract
        ↓
Research Paper 01
  formal mutation relations
  + paired fault-injection benchmark
  + reproducibility artifacts
```

This progression is intentional: the research paper extends and tests the prior engineering contract rather than re-publishing it under a new title.

## Evidence boundary

These materials describe research methodology and controlled engineering evidence. They are not investment advice, peer-reviewed performance claims, or guarantees of live trading profitability.

A passing mutation suite is not treated as proof that every leakage path is absent. Point-in-time source data, statistical validation, realistic cost and execution modeling, and independent replication remain separate requirements.

## Links

- Research hub: https://alphaquantpro.com/research
- Alpha Quant Pro: https://alphaquantpro.com
- Research Paper 01 DOI: https://doi.org/10.5281/zenodo.22052205
- Technical Note 01 DOI: https://doi.org/10.5281/zenodo.22052190

© 2026 Edmen Wong / AQP TECH ENTERPRISE. Research documentation is released under CC BY 4.0 unless otherwise stated.
