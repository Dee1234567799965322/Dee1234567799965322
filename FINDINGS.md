# Findings — one month of measuring trading indicators

*The one-line version: across ten popular signal systems and ~35,000 measured
trades, not one predicted the next move better than a coin flip. The only thing
that ever measured as non-random was trend following — and even that is marginal
after cost and only clean on instruments that don't gap.*

This is the empirical companion to the [`README`](README.md). The README tells
the story of the **harness** ([`EdgeLab.pine`](EdgeLab.pine)) and the fifteen
corrections that stopped it lying. This document is the **scoreboard**: what
every signal actually scored once those corrections were in force.

---

## The question

Do the entry signals inside popular TradingView indicators — Auction Cipher,
Market Cipher, ICT/SMC "smart money" structure, WaveTrend, divergences,
support/resistance — contain a tradeable edge, or are they decoration that
survives on confirmation bias?

To answer it you need one honest ruler, applied the same way to every signal.

## The ruler

Every signal is **paper-traded at the close of its confirmed bar** with a fixed
bracket: **target = 2 ATR (a 2R win), stop = 1 ATR (a 1R loss), give up after
100 bars**. A trade counts only when it resolves at a barrier; time-outs are
dropped, which keeps the null clean. Then five things that each killed a result
that had looked real:

1. **The null is arithmetic, not 50%.** With a 2:1 target:stop, a signal with no
   predictive power resolves as a win with probability `1/(1+2) = 33.3%`. That
   is the bar to beat.
2. **Drift is stripped by stratification.** On an asset that rises, every long
   hits +2R more often for free. So longs and shorts are measured *separately*
   and averaged — the **drift-free hit rate**. The gap between a good-looking
   long rate and a bad short rate is the asset moving, not the signal working.
3. **An edge must clear noise (MDL).** The minimum detectable live-edge is
   2.8 standard errors of the drift-free rate (Haldane–Anscombe corrected). A
   number smaller than its MDL is chance.
4. **Cost is charged in R.** ~0.05R round-trip (spread + slippage). Small gross
   edges do not survive it.
5. **One asset across five timeframes is one asset, not five** independent
   samples. Overlapping windows are pooled, not counted as replications.

## The scoreboard — ten coin flips

Every row below is measured with that ruler. `edge` is drift-free hit minus the
33.3% null; it must exceed `MDL` to count as real. **None does.**

| Signal system | Trades | Drift-free hit | Edge vs 33.3% | MDL | Verdict |
|---|---:|---:|---:|---:|---|
| **VARS** (value-area reversion) | 175 | 33.0% | −0.3pp | ±10.3 | coin flip |
| **ICT** (sweep → MSS → entry) | 407 | 34.2% | +0.9pp | ±6.6 | coin flip |
| **SMC** (IDM sweep book entry) | 303 | 31.4% | −2.0pp | ±7.5 | coin flip |
| **WaveTrend dots** (Market Cipher 9/12/3) | 2,497 | 33.7% | +0.4pp | ±2.6 | coin flip |
| **WaveTrend divergence** | 1,195 | 34.9% | +1.6pp | ±3.9 | coin flip |
| **Support/Resistance bounce** | 493 | 35.3% | +2.0pp | ±6.0 | coin flip |
| **Market Cipher A** (ribbon crosses + shapes) | 15,237 | 34.2% | +0.9pp | 0/24 charts clear | coin flip |
| Auction Cipher — 10 internal hypotheses | (see EdgeLab) | — | — | — | all killed by the 15 corrections |

The pattern is the tell: **every drift-free hit rate sits within ~2pp of 33.3%,
and the wobble shrinks toward the null exactly as the sample grows.** WaveTrend
dots over 2,497 trades land at 33.7%. Market Cipher A over 15,237 trades lands at
34.2% with not one of 24 instrument/timeframe panels clearing its noise band.
That convergence *is* the proof: there is no signal, only sampling noise around a
coin flip.

A recurring trap, made concrete on **Market Cipher A, ETH 15m**: long hit 39.9%
(looks like an edge!), short hit 28.1% (terrible), average 34.0% (dead on the
null). The 12-point gap was ETH drifting up over the window — anything long
looked good, anything short looked bad. Read only the long side and you'd have
"proof." Stratify and it vanishes. This is why people believe.

## The one exception — trend following

[`TrendRider.pine`](TrendRider.pine) is judged by a **different ruler**, because
it doesn't try to predict the next bar. Its edge, if any, lives in the *exit and
the skew*: enter with the established trend on a breakout, cut losers at 1R, let
winners run behind a chandelier stop. That produces a *low* hit rate with a large
average win — so it's scored on **expectancy, profit factor and payoff**, not hit
rate.

Pooled across **24 instrument/timeframe combos, 13,271 trades**
([`data/trendrider-test.csv`](data/trendrider-test.csv)):

- **Gross expectancy positive in 18 of 24** — real trend structure, unlike the
  ten coin flips. This is the first genuinely non-random result in the project.
- **But after a 0.05R cost, only 5 of 24 stay positive** — trade-weighted
  expectancy across the whole basket is **−0.01R**. The edge is thinner than the
  friction.
- The 5 survivors are all **daily crypto/gold** — the biggest-trending assets.
  That's drift/beta capture, regime-dependent, not repeatable per-instrument
  skill.

And the tail is the real danger. The [sweep](TrendRiderSweep.pine) and the
stop-overrun row exposed it:

- On **24/7 crypto perps** the "1R stop" is honest — worst single trades cluster
  at ~−1R (ETH −0.99R, SOL −1.03R), gap-overruns near zero.
- On **gold daily**, the same strategy took a single **−22.5R** trade when price
  gapped through the stop over a session break — that one fill *is* the entire
  −29R drawdown.

So trend following is **necessary, not sufficient**: real, but marginal after
cost, concentrated in trending majors, and account-ending at the tails unless you
run it only on continuously-traded instruments, on high timeframes, cheaply, and
sized for gap risk rather than the notional stop.

## What it means

**The edge is not in the signals.** Not in any of the ten. A month of measurement
could not find one entry trigger that beats chance. What *did* measure as real
was structural — the exit rule and the payoff skew of trend following — and it
lives on the side of trading everyone finds boring: risk management, not entries.

This matches the fifteen corrections in the README, every one of which killed a
result by fixing *how a number was compared*, never by changing trading logic.
The bottleneck in retail strategy research is not the signal. It is the
measurement.

## The deliverable that survived: Auction Cipher

The chart tool itself — [`AuctionCipher.pine`](AuctionCipher.pine) — is real work
and is kept. Over the month it was audited and hardened:

- [`AuctionCipher_watcherfix.pine`](AuctionCipher_watcherfix.pine) — correction
  19: read-time pending-watch subtraction so the dashboard rows populate live
  instead of blanking.
- [`AuctionCipher_fixed.pine`](AuctionCipher_fixed.pine) — four confirmed bugs
  from an external audit: barstate-guarded bubble roll, nPOC/LVN label
  dedent, dashboard row count, and slippage in the close-fill path.

It is a visualization, not a signal generator, and it is treated as one.

## File index

**Harness & finding**
- `EdgeLab.pine` — the measurement harness (15 corrections, `LIFT*` column)
- `TrendRider.pine` / `TrendRiderSweep.pine` — trend following + robustness sweep
- `FINDINGS.md` (this file) / `README.md` — the write-ups

**The ten coin flips**
- `ValueAreaReversion.pine`, `ICTTest.pine`, `SMCTest.pine`,
  `WaveTrendTest.pine`, `DivergenceTest.pine`, `SupportResistanceTest.pine`,
  `MarketCipherATest.pine`, plus the internal-hypothesis engines
  (`MagnetTest`, `TrapEngine`, `PositioningEngine`, `RegimeTest`, `SessionTest`,
  `ExcursionTest`, `SetupExcursion`, `InducementTest`, `SpeedLadder`)

**Chart tools & utilities**
- `AuctionCipher*.pine`, `AuctionFootprint*.pine`, `TradeJournal.pine`

**Data** — `data/*.csv`: raw resolved-trade counts behind every number above.

## Reproduce it

Load any `*Test.pine` on a chart with maximum history, read the **VERDICT** row.
For the trend system, load `TrendRider.pine` and read expectancy/PF, then
`TrendRiderSweep.pine` to check the edge is a plateau, not a single lucky
parameter. The panels print their own trade counts and withhold a verdict when
the sample is too small to answer the question.
