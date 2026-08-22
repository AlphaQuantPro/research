# Bar Time Is Not Information Time

## A Causality Contract for Quantitative Trading Pipelines

**Edmen Wong** · Alpha Quant Pro Lab Research · AQP TECH ENTERPRISE

- Technical Note 01
- Version 1.1
- Latest revision 22 August 2026
- First published 16 August 2026
- Latest version DOI: https://doi.org/10.5281/zenodo.22052190
- Concept DOI: https://doi.org/10.5281/zenodo.21965787
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

The latest DOI-bearing archival PDF is `bar-time-is-not-information-time-v1.1-doi.pdf`. The v1.0 PDF is retained for version history.

## Revision note

Version 1.1 is a branding-only revision to Alpha Quant Pro Lab naming. Research methodology, causal contract, conclusions, and evidence boundaries are unchanged from version 1.0.
