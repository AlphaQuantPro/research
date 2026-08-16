# Alpha Quant Pro Research

Public technical notes and supporting research materials from **Alpha Quant Pro** and **Alpha Tick Lab**, published by **AQP TECH ENTERPRISE**.

This repository focuses on quantitative research methodology, backtest causality, financial machine learning, walk-forward validation, execution realism, and reproducible research-to-runtime workflows.

## Technical Note 01

### Bar Time Is Not Information Time

**A Causality Contract for Quantitative Trading Pipelines**

- Author: **Edmen Wong**
- Affiliation: **AQP TECH ENTERPRISE**
- Research platform: **Alpha Tick Lab**
- Version: **1.0**
- Published: **16 August 2026**
- DOI: **10.5281/zenodo.21965788**
- Canonical research page: https://alphaquantpro.com/research/bar-time-is-not-information-time
- Zenodo record: https://doi.org/10.5281/zenodo.21965788

The note examines a less obvious class of look-ahead bias: a completed market bar can leak future information even when feature code never explicitly accesses a future row.

## Core causality contract

```text
bar_open_time < bar_close_time <= available_at
feature_time = available_at
label_end_time > feature_time
training label_end_time < validation_start
execution_time > signal_time
```

The associated validation methodology uses adversarial future-data mutation to test whether earlier features or train-owned selection evidence change when only later information is modified.

## Scope

These materials describe research methodology and engineering evidence. They are **not** investment advice, peer-reviewed performance claims, or guarantees of live trading profitability.

## Links

- Research hub: https://alphaquantpro.com/research
- Alpha Quant Pro: https://alphaquantpro.com
- DOI archive: https://doi.org/10.5281/zenodo.21965788

© 2026 Edmen Wong / AQP TECH ENTERPRISE. Research documentation is released under CC BY 4.0 unless otherwise stated.
