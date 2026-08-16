# Bar Time Is Not Information Time

## A Causality Contract for Quantitative Trading Pipelines

**Edmen Wong** · AQP TECH ENTERPRISE · Alpha Quant Pro / Alpha Tick Lab Research

- Technical Note 01
- Version 1.0
- Published 16 August 2026
- DOI: https://doi.org/10.5281/zenodo.21965788
- Canonical page: https://alphaquantpro.com/research/bar-time-is-not-information-time

## Thesis

A quantitative backtest can leak future information without explicitly reading a future row if the timestamp assigned to a completed market bar precedes the time at which the bar's final information became available.

## Boundaries covered

- completed-bar information availability
- supervised-label maturity
- train-owned and fold-local selection
- walk-forward validation leakage
- strictly-later signal execution
- adversarial future-mutation regression tests

The PDF in this directory is the DOI-bearing archival version published on Zenodo.
