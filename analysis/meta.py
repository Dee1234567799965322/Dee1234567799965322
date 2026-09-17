#!/usr/bin/env python3
"""Recompute every headline number in the measurement log from the raw counts.

    python3 analysis/meta.py

Reads data/sweeps.csv and prints the tables in the log, so any figure quoted
there can be checked rather than taken on trust. No dependencies beyond the
standard library.

The estimator is the one the panel itself uses:

    LIFT*  =  mean over the long-signal and short-signal strata of
              (signal reach - mirror reach) inside that stratum

Computed inside each stratum, it is exactly zero under drift at any long/short
mix, which raw LIFT is not. Variance is the Wald sum over strata, quartered by
the averaging.
"""
import csv, math, os

CSV = os.path.join(os.path.dirname(__file__), os.pardir, "data", "sweeps.csv")
NOISE_PP, Z_BAR, COST_R = 6.4, 3.0, 0.035


def lift_star(n_l, n_s, s_l, s_s, m_l, m_s):
    """Returns (LIFT* in pp, se in pp, long-arm, short-arm)."""
    arms, var = [], 0.0
    for n, sig, mir in ((n_l, s_l, m_l), (n_s, s_s, m_s)):
        if not n:
            continue
        p1, p2 = sig / n, mir / n
        arms.append((p1 - p2) * 100)
        var += p1 * (1 - p1) / n + p2 * (1 - p2) / n
    k = len(arms)
    return sum(arms) / k, math.sqrt(var / k**2) * 100, arms[0], arms[-1]


def mdl(se):
    """Smallest lift resolvable at 80% power against the panel's own z bar."""
    return (Z_BAR + 0.84) * se


def expectancy(lift_pp, target=2.0, cost=COST_R):
    """R per trade if the lift were real and you traded the better side."""
    p = 1 / (1 + target) + lift_pp / 200
    return p * target - (1 - p) - cost


def load():
    with open(CSV) as fh:
        return list(csv.DictReader(l for l in fh if not l.startswith("#")))


def meta(entries):
    """Fixed- and random-effects pooling. Returns a dict of everything."""
    w = [1 / se**2 for _, lf, se in entries]
    fixed = sum(x * lf for x, (_, lf, _) in zip(w, entries)) / sum(w)
    se_f = math.sqrt(1 / sum(w))
    Q = sum(x * (lf - fixed) ** 2 for x, (_, lf, _) in zip(w, entries))
    df = len(entries) - 1
    tau2 = max(0.0, (Q - df) / (sum(w) - sum(x * x for x in w) / sum(w)))
    ws = [1 / (se**2 + tau2) for _, _, se in entries]
    rand = sum(x * lf for x, (_, lf, _) in zip(ws, entries)) / sum(ws)
    se_r = math.sqrt(1 / sum(ws))
    return dict(fixed=fixed, se_f=se_f, rand=rand, se_r=se_r, Q=Q, df=df,
                tau=math.sqrt(tau2), I2=max(0.0, (Q - df) / Q) * 100 if Q else 0.0,
                pred=math.sqrt(se_r**2 + tau2))


def main():
    rows = load()
    g = lambda r, k: int(r[k]) if r[k] else 0

    print("=" * 78)
    print("PER-CHART  (LIFT* at a 2R target, against the trade's own mirror)")
    print("=" * 78)
    print(f"{'instrument':<12}{'tf':>5}{'N':>6}{'LIFT*':>8}{'se':>6}{'z*':>7}{'MDL':>7}"
          f"{'long':>7}{'short':>7}")
    for r in sorted(rows, key=lambda r: (r["tf"], r["instrument"])):
        n = g(r, "n_l") + g(r, "n_s")
        lf, se, a, b = lift_star(*[g(r, k) for k in
                                   ("n_l", "n_s", "sig_l", "sig_s", "mir_l", "mir_s")])
        print(f"{r['instrument']:<12}{r['tf']:>5}{n:>6}{lf:>+8.1f}{se:>6.2f}"
              f"{lf/se:>+7.2f}{mdl(se):>7.1f}{a:>+7.1f}{b:>+7.1f}")

    m30 = [r for r in rows if r["tf"] == "30m"]
    entries = []
    for r in m30:
        lf, se, _, _ = lift_star(*[g(r, k) for k in
                                   ("n_l", "n_s", "sig_l", "sig_s", "mir_l", "mir_s")])
        entries.append((r["instrument"], lf, se))
    M = meta(entries)
    n_tot = sum(g(r, "n_l") + g(r, "n_s") for r in m30)

    print()
    print("=" * 78)
    print(f"POOLED ACROSS {len(entries)} INSTRUMENTS AT 30m   (N = {n_tot:,} sweeps)")
    print("=" * 78)
    print(f"  fixed effect    {M['fixed']:+.2f}pp   se {M['se_f']:.2f}   z {M['fixed']/M['se_f']:+.2f}")
    print(f"  random effects  {M['rand']:+.2f}pp   se {M['se_r']:.2f}   z {M['rand']/M['se_r']:+.2f}"
          f"   CI [{M['rand']-1.96*M['se_r']:+.1f}, {M['rand']+1.96*M['se_r']:+.1f}]")
    print(f"  heterogeneity   Q {M['Q']:.1f} on {M['df']} df   I2 {M['I2']:.0f}%   tau {M['tau']:.2f}pp")
    print(f"  prediction interval for an unmeasured instrument: "
          f"[{M['rand']-2.16*M['pred']:+.1f}, {M['rand']+2.16*M['pred']:+.1f}]")
    print()
    print("  I2 above ~50% means the fixed-effect model does not apply: the")
    print("  instruments are not measuring one common quantity. Read random effects.")

    print()
    print("=" * 78)
    print("INDEPENDENCE AND PERSISTENCE   (charts where both were captured)")
    print("=" * 78)
    print(f"{'instrument':<12}{'tf':>5}{'full':>8}{'no-overlap':>12}{'z':>7}"
          f"{'1st half':>10}{'2nd half':>10}{'diff z':>8}  verdict")
    for r in rows:
        if not r["i_n_l"] or not r["h1"]:
            continue
        lf, _, _, _ = lift_star(*[g(r, k) for k in
                                  ("n_l", "n_s", "sig_l", "sig_s", "mir_l", "mir_s")])
        ilf, ise, _, _ = lift_star(*[g(r, k) for k in
                                     ("i_n_l", "i_n_s", "i_sig_l", "i_sig_s",
                                      "i_mir_l", "i_mir_s")])
        h1, h2, hz = float(r["h1"]), float(r["h2"]), float(r["hz"])
        # correction 12: significance before sign
        v = ("FLIPS" if abs(hz) > 2 and h1 * h2 < 0 else
             "unstable" if abs(hz) > 2 else
             "sign not established" if h1 * h2 < 0 else "stable")
        print(f"{r['instrument']:<12}{r['tf']:>5}{lf:>+8.1f}{ilf:>+12.1f}{ilf/ise:>+7.2f}"
              f"{h1:>+10.1f}{h2:>+10.1f}{hz:>+8.2f}  {v}")

    print()
    print("=" * 78)
    print("WHAT ANY OF IT WOULD BE WORTH   (2R target)")
    print("=" * 78)
    need = lambda pp: math.ceil(2 * (1/3) * (2/3) * (3.84 / (pp / 100)) ** 2)
    print(f"  at 2R a {COST_R}R round trip costs {((1+COST_R)/3 - 1/3) * 200:.1f}pp of lift "
          f"before anything is left over")
    for pp in (3.0, 4.0, 6.4, 9.9):
        print(f"    {pp:>4.1f}pp -> {expectancy(pp):+.3f} R/trade"
              f"   ({expectancy(pp)*300:+6.1f} R/yr at 300 trades)"
              f"   needs N = {need(pp):,}")
    print()
    print(f"  The noise floor is {NOISE_PP}pp, measured feed-to-feed on one asset.")
    print("  Anything under it is which exchange you happened to load.")


if __name__ == "__main__":
    main()
