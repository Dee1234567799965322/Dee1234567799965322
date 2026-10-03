# Findings — one month of measuring trading indicators

*The one-line version: across a dozen popular signal systems and well over 35,000
measured trades, not one predicted the next move better than a coin flip. Even
stacking two signals — the best-motivated attempt, a liquidity sweep confirmed by
order-flow delta — changed nothing: two coin flips don't make a weighted coin. The
only thing that ever measured as non-random was trend following, and even that is
marginal after cost and only clean on instruments that don't gap. The one
constructive build ([`TrendParticipation.pine`](TrendParticipation.pine)) doesn't
predict at all: it cuts drawdown 3–4× vs buy-and-hold, which is a calmer ride, not
more money.*

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

## The scoreboard — a dozen coin flips

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
| **Trend Stack** (implied pullback-resume) | see note | ~40% at N≥30 | +5–8pp | ±24 | coin flip |
| **SFP + Volume Delta** (LuxAlgo confluence) | 975 | 32.4% | −0.9pp | ±4.3 | coin flip |
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

## The clearest lesson — the small-sample mirage

The eleventh signal, **Trend Stack**, produced the single best demonstration in
the project of *why* the ruler needs every one of its parts. On **gold 4h**, its
implied pullback-resume entry showed a **67.9% drift-free hit rate and +0.99R per
trade** — a number people mortgage the house on. It was **19 trades**, with an MDL
of **±33pp**: the confidence interval ran from ~35% to ~100%, so the panel
withheld the verdict (`NEED MORE DATA`) rather than paint it green.

Drop to a timeframe where the same signal clears 30 trades — **gold 1h and BTC
1h/30m** — and the 68% **collapsed to ~40%**, the verdict flipping to COIN FLIP
([`data/trendstack-test.csv`](data/trendstack-test.csv)). The spectacular
high-timeframe number was small-sample luck evaporating as the sample grew, the
same convergence-to-33.3% caught in the act.

The lesson generalises past this one indicator: **every** signal will hand you a
window where it looks like a miracle. Without a fixed null, drift stratification,
and a sample-size gate that refuses to bless a number it cannot yet distinguish
from luck, you do not measure edges — you collect mirages. That gate is the most
important line on the panel.

A note of credit: Trend Stack itself is one of the *better* tools reviewed —
honest that it is a dashboard, correct percentile bands (not fake 2-SD), and it
fires no buy/sell arrows. Only the entry buried in its comments, which it wisely
never actually fires, is the coin flip. The author was right not to ship it.

## The confluence test — SFP + Volume Delta

The best-motivated combination the project tried, built from two LuxAlgo tools
([`SFPDeltaConfluence.pine`](SFPDeltaConfluence.pine)): the **Swing Failure
Pattern** (a liquidity sweep — price pierces a swing then closes back inside) says
*where* a trap sprang; **Volume Delta** (net intrabar buying/selling, reconstructed
from a lower timeframe) says *who* won it. The thesis: a bullish sweep *with* net
buying is a sweep the buyers absorbed → long; mirror for shorts. If any confluence
should beat a lone signal, this one should.

It was measured as a full matrix on BTC perp — four timeframes × the delta filter
ON (SFP + Δ) vs OFF (pure SFP) — with an explicit **`Delta gate: ON/OFF`** row
added to the panel so each run states its own configuration rather than leaving it
to be inferred:

| TF | Gate ON (SFP + Δ) | Gate OFF (pure SFP) |
|---|---|---|
| **15m** | 78 · 32.1% · coin flip | 185 · 29.7% · coin flip |
| **30m** | 49 · 36.9% · coin flip | **406 · 34.5% · coin flip** |
| **1h** | **18 · 55.6% · need more data** | **191 · 34.0% · coin flip** |
| **4h** | 6 · 50.0% · need more data | 193 · 29.1% · coin flip |

Two things fall out, and both matter:

**The delta confirmation is cosmetic.** Same chart, flip the gate: requiring delta
to agree roughly *halves* the trade count (30m: 406 → 49; 1h: 191 → 18) and never
moves the verdict. It removes trades, it does not predict them. Stacking a second
coin flip on the first gives you a smaller coin flip, not an edge — proven here
side by side with the gate row as witness.

**It is also the cleanest small-sample mirage in the file.** Read the 1h row
across: gate ON shows **55.6% on 18 trades** (`need more data`, MDL ±32.8) — the
exact kind of number that sells a strategy. Turn the gate OFF, the sample grows 10×
to **191 trades, and the hit rate falls to 34.0%** — a hair above the 33.3% null.
The 55.6% was never an edge; it was delta shrinking the sample until noise looked
like signal. The **30m pure-SFP run (406 trades, edge +1.2pp against an MDL of
±6.6)** is the single most statistically solid null in the entire project: the
observed edge is a fifth of what it would need to clear chance, with no sample-size
wiggle room left. Pooled across all four pure-SFP timeframes — **975 resolved
trades, drift-free 32.4%, −0.9pp** — the sweep is a coin flip, full stop.

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

## The constructive answer — Trend Participation

[`TrendParticipation.pine`](TrendParticipation.pine) is what the whole month
points at once you stop looking for a predictor. It contains **no entry signal**.
It participates in drift while the slow trend is up, sizes every position by
volatility so risk stays constant (never leveraged by default), trails out wide
to keep the fat tail, and — crucially — **judges itself against buy-and-hold, not
a coin flip**, on return per unit of drawdown. On a drifting asset, holding is the
real benchmark.

Measured on daily history ([`data/trend-participation-test.csv`](data/trend-participation-test.csv)):

| Asset | Strat return | Hold return | Strat max DD | Hold max DD | Return/DD | vs hold |
|---|---:|---:|---:|---:|---|---|
| **SOLUSDT.P** | +212% | +514% | **−25%** | −96% | 8.55 vs 5.34 | wins both |
| **ETHUSDT.P** | +283% | +1027% | **−23%** | −79% | 12.08 vs 12.95 | ties |
| **BTCUSDT.P** | +306% | +1141% | **−24%** | −77% | 12.69 vs 14.88 | ties |

The one real, repeatable effect: it holds max drawdown to **~−24% on every
asset** while buy-and-hold suffered **−77% to −96%** — a 3–4× reduction, and
(confirmed at max leverage 1) **not** a leverage artifact. The cost is that it
keeps only a quarter to a third of the raw return, so on BTC/ETH its risk-adjusted
return merely *ties* holding; only SOL, whose hold drawdown was catastrophic,
wins outright.

The honest reading: **this is not alpha and not more money. It is a way to take a
much calmer ride to roughly the same place** — a −24% drawdown a human can
actually sit through instead of an −80% one they panic-sell. That behavioural
survivability, on assets that trend and don't gap, sized small and diversified, is
the only defensible reason to trade that a month of measurement produced.
Caveats stand: ~35–48 trades over a bull-heavy era, untested in a true multi-year
bear. The only test left is forward.

## What it means

**The edge is not in the signals.** Not in any of the eleven. A month of
measurement could not find one entry trigger that beats chance. What *did* measure as real
was structural — the exit rule and the payoff skew of trend following — and it
lives on the side of trading everyone finds boring: risk management, not entries.

This matches the fifteen corrections in the README, every one of which killed a
result by fixing *how a number was compared*, never by changing trading logic.
The bottleneck in retail strategy research is not the signal. It is the
measurement.

## The deliverable that survived: Auction Cipher

The chart tool itself — [`AuctionCipher.pine`](AuctionCipher.pine) — is real work
and is kept. Over the month it was audited and hardened, and all fixes are now
consolidated into that single canonical file:

- **Correction 19** — read-time pending-watch subtraction so the dashboard rows
  populate live instead of blanking.
- **Four confirmed bugs from an external audit** — barstate-guarded bubble roll,
  nPOC/LVN label dedent, dashboard row count, and slippage in the close-fill path.

(The intermediate `_watcherfix` and `_fixed` builds have been folded into
`AuctionCipher.pine` and retired.) It is a visualization, not a signal generator,
and it is treated as one.

## File index

**Harness & finding**
- `EdgeLab.pine` — the measurement harness (15 corrections, `LIFT*` column)
- `TrendRider.pine` / `TrendRiderSweep.pine` — trend following + robustness sweep
- `TrendParticipation.pine` — the constructive build: drift capture + drawdown control, judged vs buy-and-hold
- `FINDINGS.md` (this file) / `README.md` — the write-ups

**The eleven coin flips**
- `ValueAreaReversion.pine`, `ICTTest.pine`, `SMCTest.pine`,
  `WaveTrendTest.pine`, `DivergenceTest.pine`, `SupportResistanceTest.pine`,
  `MarketCipherATest.pine`, `TrendStackTest.pine`, `SFPDeltaConfluence.pine`,
  plus the internal-hypothesis
  engines (`MagnetTest`, `TrapEngine`, `PositioningEngine`, `RegimeTest`,
  `SessionTest`, `ExcursionTest`, `SetupExcursion`, `InducementTest`,
  `SpeedLadder`)

**Chart tools & utilities**
- `AuctionCipher*.pine`, `AuctionFootprint*.pine`, `TradeJournal.pine`

**Data** — `data/*.csv`: raw resolved-trade counts behind every number above.

## Reproduce it

Load any `*Test.pine` on a chart with maximum history, read the **VERDICT** row.
For the trend system, load `TrendRider.pine` and read expectancy/PF, then
`TrendRiderSweep.pine` to check the edge is a plateau, not a single lucky
parameter. The panels print their own trade counts and withhold a verdict when
the sample is too small to answer the question.
