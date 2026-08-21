#!/usr/bin/env python3
"""Reference mutation benchmark for AITT Research Paper 01."""
from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
import pandas as pd
from scipy.stats import beta
from sklearn.linear_model import LinearRegression

N = 4096
PHIS = np.array([0.65, 0.40, 0.20, -0.25, 0.0])
HORIZON = 20
CUTOFF_FRACTIONS = (0.4, 0.6, 0.8)
TOL = 1e-10


def generate_series(seed: int, n: int = N) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed)
    x = np.zeros((n, 5))
    eps = rng.normal(size=(n, 5))
    for t in range(1, n):
        x[t] = PHIS * x[t - 1] + eps[t]
    eta = rng.normal(size=n)
    r = np.zeros(n)
    for t in range(2, n):
        r[t] = 0.18 * x[t - 1, 0] - 0.12 * x[t - 2, 1] + 0.08 * x[t - 1, 2] + eta[t]
    return x, r

def trailing_feature(x: np.ndarray) -> np.ndarray:
    return pd.Series(x).shift(1).rolling(21, min_periods=21).mean().to_numpy()


def centered_feature(x: np.ndarray) -> np.ndarray:
    return pd.Series(x).rolling(21, center=True, min_periods=21).mean().to_numpy()


def expanding_normalization(x: np.ndarray) -> np.ndarray:
    s = pd.Series(x)
    hist = s.shift(1)
    mu = hist.expanding(min_periods=20).mean()
    sigma = hist.expanding(min_periods=20).std(ddof=0)
    return ((s - mu) / sigma).to_numpy()


def full_sample_normalization(x: np.ndarray) -> np.ndarray:
    return (x - x.mean()) / x.std(ddof=0)


def select_feature(x: np.ndarray, r: np.ndarray, idx: np.ndarray) -> int:
    scores = []
    for j in range(x.shape[1]):
        corr = np.corrcoef(x[idx, j], r[idx])[0, 1]
        scores.append(abs(corr))
    return int(np.nanargmax(scores))


def forward_labels(r: np.ndarray, horizon: int = HORIZON) -> np.ndarray:
    y = np.full(len(r), np.nan)
    csum = np.concatenate([[0.0], np.cumsum(r)])
    for t in range(len(r) - horizon):
        y[t] = csum[t + horizon + 1] - csum[t + 1]
    return y


def supervised_artifact(x: np.ndarray, r: np.ndarray, cutoff: int, maturity_aware: bool) -> np.ndarray:
    y = forward_labels(r)
    if maturity_aware:
        eligible = np.arange(0, cutoff - HORIZON + 1)
    else:
        eligible = np.arange(0, cutoff + 1)
    eligible = eligible[~np.isnan(y[eligible])]
    model = LinearRegression().fit(x[eligible, :3], y[eligible])
    pred = model.predict(x[: cutoff + 1, :3])
    return np.concatenate([[model.intercept_], model.coef_, pred])


def clean_bar_artifact(raw: np.ndarray, cutoff: int, width: int = 5) -> np.ndarray:
    values = []
    for open_idx in range(0, len(raw) - width + 1, width):
        close_idx = open_idx + width - 1
        if close_idx <= cutoff:
            values.append(raw[open_idx : close_idx + 1].mean())
    return np.asarray(values, dtype=float)


def leaky_open_stamped_bar_artifact(raw: np.ndarray, cutoff: int, width: int = 5) -> np.ndarray:
    values = []
    for open_idx in range(0, len(raw) - width + 1, width):
        if open_idx <= cutoff:
            values.append(raw[open_idx : open_idx + width].mean())
    return np.asarray(values, dtype=float)

def generate_execution_events(seed: int, n_days: int = 2048) -> tuple[np.ndarray, np.ndarray]:
    rng = np.random.default_rng(seed + 999_999)
    open_px = rng.normal(100.0, 2.0, size=n_days)
    close_px = open_px + rng.normal(0.0, 1.0, size=n_days)
    return open_px, close_px


def clean_next_open_positions(open_px: np.ndarray, close_px: np.ndarray, cutoff_day: int) -> np.ndarray:
    pos = np.zeros(cutoff_day + 1)
    for d in range(1, cutoff_day + 1):
        pos[d] = np.sign(close_px[d - 1] - open_px[d - 1])
    return pos


def leaky_same_open_positions(open_px: np.ndarray, close_px: np.ndarray, cutoff_day: int) -> np.ndarray:
    return np.sign(close_px[: cutoff_day + 1] - open_px[: cutoff_day + 1]).astype(float)


def max_deviation(a: np.ndarray, b: np.ndarray) -> float:
    if len(a) == 0 and len(b) == 0:
        return 0.0
    if a.shape != b.shape:
        return float("inf")
    finite = np.isfinite(a) & np.isfinite(b)
    if not finite.any():
        return 0.0
    return float(np.max(np.abs(a[finite] - b[finite])))


def add_trial(rows: list[dict], fixture: str, status: str, mutation: str, seed: int, frac: float, dev: float) -> None:
    rows.append({"fixture": fixture, "status": status, "mutation": mutation, "seed": seed,
                 "cutoff_fraction": frac, "max_deviation": dev, "violation": bool(dev > TOL)})

def run_benchmark(n_seeds: int = 200) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    rows: list[dict] = []
    targeted_rows: list[dict] = []

    for seed in range(n_seeds):
        x, r = generate_series(seed)
        for frac in CUTOFF_FRACTIONS:
            cutoff = int(frac * N) - 1

            rng = np.random.default_rng(seed * 1000 + int(frac * 100))
            x_mut = x.copy()
            x_mut[cutoff + 1 :, 0] += rng.normal(0.0, 8.0, size=N - (cutoff + 1))

            dev = max_deviation(
                trailing_feature(x[:, 0])[: cutoff + 1],
                trailing_feature(x_mut[:, 0])[: cutoff + 1],
            )
            add_trial(rows, "C1 trailing rolling mean", "causal", "future Gaussian X0", seed, frac, dev)

            dev = max_deviation(
                centered_feature(x[:, 0])[: cutoff + 1],
                centered_feature(x_mut[:, 0])[: cutoff + 1],
            )
            add_trial(rows, "L1 centered rolling mean", "leaky", "future Gaussian X0", seed, frac, dev)

            dev = max_deviation(
                expanding_normalization(x[:, 0])[: cutoff + 1],
                expanding_normalization(x_mut[:, 0])[: cutoff + 1],
            )
            add_trial(rows, "C2 expanding normalization", "causal", "future Gaussian X0", seed, frac, dev)

            dev = max_deviation(
                full_sample_normalization(x[:, 0])[: cutoff + 1],
                full_sample_normalization(x_mut[:, 0])[: cutoff + 1],
            )
            add_trial(rows, "L2 full-sample normalization", "leaky", "future Gaussian X0", seed, frac, dev)

            rng_sel = np.random.default_rng(seed * 2000 + int(frac * 100))
            x_sel = x.copy()
            x_sel[cutoff + 1 :, 4] = 6.0 * r[cutoff + 1 :] + rng_sel.normal(
                0.0, 0.1, size=N - (cutoff + 1)
            )

            j0 = select_feature(x, r, np.arange(2, cutoff + 1))
            j1 = select_feature(x_sel, r, np.arange(2, cutoff + 1))
            art0 = np.concatenate([[j0], x[: cutoff + 1, j0]])
            art1 = np.concatenate([[j1], x_sel[: cutoff + 1, j1]])
            dev = max_deviation(art0, art1)
            add_trial(rows, "C3 fold-local feature selection", "causal", "future-only predictive X5", seed, frac, dev)

            j0 = select_feature(x, r, np.arange(2, N))
            j1 = select_feature(x_sel, r, np.arange(2, N))
            art0 = np.concatenate([[j0], x[: cutoff + 1, j0]])
            art1 = np.concatenate([[j1], x_sel[: cutoff + 1, j1]])
            dev = max_deviation(art0, art1)
            add_trial(rows, "L3 global feature selection", "leaky", "future-only predictive X5", seed, frac, dev)

            rng_lab = np.random.default_rng(seed * 3000 + int(frac * 100))
            r_mut = r.copy()
            r_mut[cutoff + 1 :] += rng_lab.normal(0.0, 10.0, size=N - (cutoff + 1))

            dev = max_deviation(
                supervised_artifact(x, r, cutoff, True),
                supervised_artifact(x, r_mut, cutoff, True),
            )
            add_trial(rows, "C4 maturity-aware training", "causal", "future Gaussian returns", seed, frac, dev)

            dev = max_deviation(
                supervised_artifact(x, r, cutoff, False),
                supervised_artifact(x, r_mut, cutoff, False),
            )
            add_trial(rows, "L4 row-index-only label eligibility", "leaky", "future Gaussian returns", seed, frac, dev)

            raw = x[:, 0].copy()
            rng_bar = np.random.default_rng(seed * 4000 + int(frac * 100))
            raw_mut = raw.copy()
            raw_mut[cutoff + 1 :] += rng_bar.normal(0.0, 8.0, size=N - (cutoff + 1))

            dev = max_deviation(clean_bar_artifact(raw, cutoff), clean_bar_artifact(raw_mut, cutoff))
            add_trial(rows, "C5 availability-aware completed bar", "causal", "future Gaussian raw events", seed, frac, dev)

            dev = max_deviation(
                leaky_open_stamped_bar_artifact(raw, cutoff),
                leaky_open_stamped_bar_artifact(raw_mut, cutoff),
            )
            add_trial(rows, "L5 open-stamped completed bar", "leaky", "future Gaussian raw events", seed, frac, dev)

            open_px, close_px = generate_execution_events(seed)
            cutoff_day = int(frac * len(open_px)) - 1
            rng_exec = np.random.default_rng(seed * 5000 + int(frac * 100))
            close_mut = close_px.copy()
            close_mut[cutoff_day:] += rng_exec.normal(0.0, 10.0, size=len(close_px) - cutoff_day)

            dev = max_deviation(
                clean_next_open_positions(open_px, close_px, cutoff_day),
                clean_next_open_positions(open_px, close_mut, cutoff_day),
            )
            add_trial(rows, "C6 next-open execution", "causal", "random unavailable close mutation", seed, frac, dev)

            dev = max_deviation(
                leaky_same_open_positions(open_px, close_px, cutoff_day),
                leaky_same_open_positions(open_px, close_mut, cutoff_day),
            )
            add_trial(rows, "L6 same-open retro-execution", "leaky", "random unavailable close mutation", seed, frac, dev)

            targeted = close_px.copy()
            delta = close_px[cutoff_day] - open_px[cutoff_day]
            sign = 1.0 if delta >= 0 else -1.0
            targeted[cutoff_day] = open_px[cutoff_day] - sign * (abs(delta) + 1.0)
            dev = max_deviation(
                leaky_same_open_positions(open_px, close_px, cutoff_day),
                leaky_same_open_positions(open_px, targeted, cutoff_day),
            )
            targeted_rows.append({
                "fixture": "L6 same-open retro-execution", "status": "leaky",
                "mutation": "targeted sign-flip unavailable close", "seed": seed,
                "cutoff_fraction": frac, "max_deviation": dev, "violation": bool(dev > TOL),
            })

    trials = pd.DataFrame(rows)
    targeted_df = pd.DataFrame(targeted_rows)
    summary = (
        trials.groupby(["fixture", "status", "mutation"], as_index=False)
        .agg(
            trials=("violation", "size"),
            violations=("violation", "sum"),
            violation_rate=("violation", "mean"),
            median_max_deviation=("max_deviation", "median"),
            mean_max_deviation=("max_deviation", "mean"),
            min_max_deviation=("max_deviation", "min"),
            max_max_deviation=("max_deviation", "max"),
        )
    )
    return trials, summary, targeted_df


def clopper_pearson(x: int, n: int, alpha: float = 0.05) -> tuple[float, float]:
    lower = 0.0 if x == 0 else float(beta.ppf(alpha / 2, x, n - x + 1))
    upper = 1.0 if x == n else float(beta.ppf(1 - alpha / 2, x + 1, n - x))
    return lower, upper


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seeds", type=int, default=200)
    parser.add_argument("--out", type=Path, default=Path("results"))
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    trials, summary, targeted = run_benchmark(args.seeds)
    trials.to_csv(args.out / "trials.csv", index=False)
    summary.to_csv(args.out / "summary.csv", index=False)
    targeted.to_csv(args.out / "execution_targeted.csv", index=False)

    print(summary.to_string(index=False))
    x = int(targeted["violation"].sum())
    n = len(targeted)
    lo, hi = clopper_pearson(x, n)
    print()
    print(f"Targeted execution adversary: {x}/{n} ({x/n:.4f}), 95% CI [{lo:.4f}, {hi:.4f}]")


if __name__ == "__main__":
    main()
