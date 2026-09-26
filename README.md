# Auction Cipher — an indicator, and ten attempts to find an edge in it

Twelve Pine v6 files. One is a chart tool. Ten are experiments that failed.
The eleventh is the harness that explains why, and it is the only one worth
carrying forward.

Full measurement record, with every table and the reasoning behind each
correction: **https://claude.ai/artifact/TMma7a41v7WELDWNe36FPh**

---

## Start here

**`EdgeLab.pine`** — the harness. It contains no signal, because none of the
ten hypotheses produced one. What it contains is the ten corrections that
killed them, wired in as gates a result has to pass before the panel will call
it an edge.

Defaults are set for **XAUUSD 30m**: 1 ATR stop, 200-bar horizon, 0.035R cost,
2R target. Load maximum history before reading anything — the panel prints its
own bar count and will say `UNDERPOWERED` when the sample cannot resolve the
question, which on a default chart is most of the time.

Read one column: **`LIFT*`**. Everything else on the panel exists to stop
`LIFT*` from lying.

---

## The fifteen corrections

Each one killed a result that looked real. Four killed results that had already
been written up.

| # | Correction | What it killed |
|---|---|---|
| 1 | **The mirror** — every signal opens its own opposite, same bar, same risk | "Poor high revisited 80%". The mirror baseline is 76% |
| 2 | **The null is arithmetic** — `1/(1+n)`, not estimated | "Cut losses, let winners run": zero at every target over 8,302 trades |
| 3 | **The noise floor is 6.4pp**, measured feed-to-feed on one asset | Every result smaller than two exchanges' disagreement with each other |
| 4 | **Multiplicity** — the z bar rises with the cell count | `z = 2.25` across 15 cells: 31% likely by chance |
| 5 | **Censoring and cost in R** | The speed ladder, unreadable; every crypto result, on cost alone |
| 6 | **Direction stratification** (`LIFT*` inside each stratum) | Nothing at 30m, where buckets were balanced — then 1.3pp of gold's 4h result, exactly as the algebra predicted |
| 7 | **Power** — state the smallest effect the sample could see | Six "nulls" that were empty instruments rather than measurements |
| 8 | **Fix the target rung before looking** | A verdict that picked its own best cell and reported a different cell's power |
| 9 | **Non-overlapping trades only** | The pooled `z = −3.12` — the one number that cleared the bar |
| 10 | **Split-half persistence** | Gold's −9.7pp and GBPJPY's −6.3pp. Both were windows, not instruments |
| 11 | **Resolution invariance** — does it survive changing the bar size? | Bitcoin, the last survivor — then gold, whose −9.6pp at 30m is a lone spike among +3.9, +4.6, −4.2 |
| 12 | Test significance **before** sign, in the persistence verdict | A false `FLIPS` on gold 15m: +11.7 vs −1.7 at z 1.45 |
| 13 | The same in the independence verdict, and require the full sample to have made a claim | A false `DISAGREES` on gold 5m: "the full-sample z was overlap" where that z was +0.84 |
| 14 | The same again in the **colours** | 27 cells painted as findings across the whole project. **None cleared the gate printed two lines below them** |
| 15 | The colour must apply the **sample** gates too, not just the z | The first green cell ever produced — one run after correction 14 shipped, and a false positive |

Four of the fifteen are about the *denominator* — what a number is compared
against, and how many chances it had. Two are about what counts as one
observation. One is about whether the thing being measured belongs to the market
or to the chart. Three are the panel caught making the exact mistake it exists to prevent — in
three consecutive passes, each in a different part of the same file, all written
before the standard existed and none revisited when it did. **A standard added
late does not propagate backwards through the code that preceded it** — that is
the most transferable thing here, and it took three rounds to learn.
**None is about trading logic.** Every result this repo lost,
it lost to measurement.

### Gold across four bar sizes

| Chart | N | LIFT* | z* |
|---|---|---|---|
| 5 minutes | 208 | +3.9pp | +0.84 |
| 15 minutes | 213 | +4.6pp | +1.00 |
| **30 minutes** | 303 | **−9.6pp** | **−2.53** |
| 4 hours | 189 | −4.2pp | −0.86 |

A single spike at 30m between near-zero neighbours — and 30m is the timeframe
this whole investigation was built on. This repo's own log had already named
that shape, about the *original* result: *"an isolated spike between a zero and
a negative is what a single lucky cell looks like."*

Caveat that cuts both ways: the four charts are four different experiments, not
four views of one. Stop is 1 ATR *of that timeframe* and horizon is 200 bars *of
that timeframe*, so bar size, stop size and holding window move together. What
the ladder establishes is that the **sign of the answer is set by the
parameterisation** — which is fatal either way. An effect that inverts when you
change a chart setting is a parameter choice, not an edge.

### The test that closed the circle

Bitcoin was the last instrument standing: −8.2pp at 30m, stable across both
halves of its chart, same sign on non-overlapping trades, failing only on cost.
Run at **15 minutes** it reads **+8.5pp** — nearly equal magnitude, opposite
sign, `z = 3.20` apart. That gap is the only thing in this project that ever
cleared the 3.0 bar, and it is a contradiction rather than a result.

Not a period artefact either: the 15m window sits inside the 30m chart's second
half, where 30m says −7.8pp and 15m says +8.4pp over the same days.

**Both cells pass split-half persistence individually.** Correction 10 asks
whether an effect is stable in *time* and says yes to both; it cannot see that
they disagree with each other. A sweep is supposed to be resting stops being
taken — if it were, halving the bar size would not invert it. What inverts
under resampling is a property of the chart, not the auction.

This is the same diagnostic that killed the original Auction Cipher result
(gold +41.1R at 30m, −14.1R at 15m). Ten hypotheses later the last survivor
died the same way.

---

## The files

### Kept

| File | What it is |
|---|---|
| `EdgeLab.pine` | The harness above. Six setup buckets, each against its own mirror, with all ten corrections enforced |
| `AuctionCipher.pine` | The original v3.0 indicator, 5,606 lines. A good chart tool. Audited clean; its R accounting reconciles by construction |
| `AuctionFootprint.pine` | Companion footprint/volume-profile renderer |
| `ValueAreaReversion.pine` | A third-party value-area reclaim indicator (SFP family), with the measurement panel bolted on so it reports its own hit rate against `1/(1+R)` instead of being argued about. Result pending |
| `ICTTest.pine` | The full ICT sequence assembled — liquidity sweep, then market-structure shift, then entry — measured as one setup rather than as separate primitives. Its parts were each measured flat or negative elsewhere in this log; this tests whether the sequence is more than their sum. Same measurement panel. Result pending |
| `SMCTest.pine` | The World Class SMC *primary* entry from the source PDFs — break of structure, then an inducement (IDM) sweep by an IFC candle, entering in the trend direction, with an optional imbalance filter. This is trend continuation, distinct from ICTTest's reversal. Same measurement panel. Result pending |
| `WaveTrendTest.pine` | The buy/sell dots from the Liquidity Tracker's oscillator (Market Cipher 9/12/3 on hlc3), measured with the standard panel. The WaveTrend engine is copied verbatim so the dots are identical; the rest of that indicator draws context levels and makes no directional claim. Result pending |
| `TradeJournal.pine` | Turns the measurement panel on the user's own discretionary entries. Log each real trade as a slot (Long/Short + entry time); it opens a synthetic 2R trade at that bar and scores your entries against the same 1/(1+R) null as every signal test. The last unmeasured input, and the only one honesty rather than code has to guarantee. |
| `SupportResistanceTest.pine` | The oldest idea in trading: buy the bounce off support, sell the rejection at resistance, where a level is a confirmed swing pivot. Long when price holds a prior swing low, short when it rejects a prior swing high. Each level arms one bounce then is spent. Same measurement panel. Result pending |
| `DivergenceTest.pine` | The WaveTrend divergence signal from the Liquidity Tracker, reproduced verbatim. Bullish = price lower low while the oscillator makes a higher low (long); bearish = price higher high, oscillator lower high (short). Money-flow confirmation optional. Same measurement panel. Result pending |
| `TrendRider.pine` | Not another entry signal. Time-series momentum: enter with the trend on a Donchian breakout, cut losers at 1R, let winners run behind a chandelier trailing stop. Judged by expectancy, profit factor and payoff (win/loss) rather than hit rate, because a trend system is meant to have a low hit rate and a large average win. The one approach in this repo with a real out-of-sample track record; its edge is in the exit and the skew, not the entry |

### The experiments, in the order they were run

| File | Hypothesis | Trades | Result |
|---|---|---|---|
| `TrapEngine.pine` | Sweeps and reclaims force exits | 512 | −0.7pp, z −0.34 |
| `PositioningEngine.pine` | Open interest reveals forced closure | 408 | −1.0pp, z −0.42 |
| `MagnetTest.pine` | Structural levels attract price | 1,567 pairs | −5.4pp, z −2.25 — *backwards from theory* |
| `RegimeTest.pine` | Extreme quality classifies regime | 217 calls | −6.4pp, z −1.90 — wrong more often than drift |
| `SessionTest.pine` | The clock and the initial balance | 2,478 | +0.17pp, then −0.15pp on a rerun |
| `ExcursionTest.pine` | Fat right tails pay for bad entries | 8,302 | Every target within 0.40pp of `1/(1+n)` |
| `SetupExcursion.pine` | Real setups beat timer entries | 4,356 | 18 of 20 cells negative |
| `InducementTest.pine` | The two-stage liquidity grab | 406 induced | Less bad than plain sweeps, not better than random |
| `SpeedLadder.pine` | Stop width changes the answer | ~20,000 | Confounded by censoring — see correction 5 |

`ExcursionTest` and `SetupExcursion` are the two results worth trusting on
their own: both had the sample size to make the claim they made. The rest were
underpowered and said nothing about it, which is why correction 7 exists.

---

## What was actually found

Not "no edge" — something narrower:

> Swept levels are **followed slightly more often than they are faded**, by
> roughly 3–4 percentage points at a 2R target. The sign survives direction
> stratification, non-overlapping sampling, and split-half on three of five
> instruments.

It is also smaller than the 6.4pp noise floor, worth about **+0.02R per trade**
against a 0.035R CFD cost, and would need roughly **4,100 sweeps — about nine
years of 30-minute history** — to establish at the standard `EdgeLab` enforces.

### Raising the timeframe does not help

Sweeps arrive at a near-constant rate per bar — 1 per 27.8 bars at 30m, 1 per
30.4 at 4h — so sample size is set by how many bars the platform will load, and
it loads fewer at 4h. The test gets *weaker* going up:

| Chart | Bars | Sweeps | Smallest lift resolvable |
|---|---|---|---|
| XAUUSD 30m | 8,413 | 303 | 14.7pp |
| XAUUSD 4h | 5,744 | 189 | 18.6pp |

Resolving the noise floor at 4h would take about **22 years** of gold. 30m is
the sweet spot, not a compromise.

The 4h run did earn one thing: it is the only sample where drift (+10.9pp) and
bucket skew (83/106) were both large enough for correction 6 to bite. Predicted
artefact `skew × drift = −1.33pp`; observed raw-minus-`LIFT*` difference
`−1.11pp`. The correction removes what the arithmetic says it should.

Across 14 instruments the between-instrument spread is **τ = 4.4pp**, larger
than the pooled effect itself, and the effect also varies *within* an instrument
across time (2 of 5 flip sign between chart halves, p = 0.023). So a
full-sample number for any single chart is an average over regimes that will
not repeat.

---

## Pine v6 traps this repo hit

Recorded because each one cost real time and none announces itself.

- **`ta.*` functions carry rolling state.** Reached behind an `and` or a
  ternary they silently return stale values. Call them top-level and
  unconditional.
- **Functions cannot assign globals.** Mutate arrays and return values instead.
- **`for i = 0 to arr.size() - 1` on an empty array runs `i = 0` then `i = -1`**
  and throws on the first `get`. Guard every loop.
- **Scalars roll back on realtime bars; arrays and drawings do not.** Gate all
  persistent mutation on `barstate.isconfirmed`.
- **`plotchar(cond ? true : na)` is a type error** — Pine will not unify `bool`
  with `na`. Pass the bool series directly.
- **A name may not be reused across types** in the same scope (a `table` and a
  `float` called `st` will not compile).
- **`str.tostring(-9.1, "+#.#")` renders `-+9.1`** — the forced plus is emitted
  after the minus. Sign numbers in code and let the format carry digits only.
- **`//@version=6` must be line 1**, and `indicator()` must precede any
  `import`.
- `AuctionCipher.pine` sits at ~2,171 main-body statements against a compile
  limit near 2,180. Anything added there has to live inside a function body.

---

## Reading an EdgeLab panel

| Row | Says |
|---|---|
| `TIMER (drift)` | The sample's drift. Its `LIFT` is long-minus-short on entries with no view at all |
| `LIFT` | Raw. Still carries `skew × drift` |
| `LIFT*` | Computed inside each direction. Drift-free at any long/short mix. **Read this one** |
| `MDL` | Smallest lift this sample could resolve at 80% power. Orange means the bucket cannot answer the question, whatever else it prints |
| `Partition` | `INDUCED + PLAIN` must equal `SWEEP`. If it does not, the classifier is broken and every number above it is wrong |
| `POOL` | Raw stratum counts, so several instruments can be meta-analysed exactly |
| `SPLIT` | First half against second half. `FLIPS` means the effect belongs to the window, not the instrument |
| `IND` | Trades that never shared a bar. `DISAGREES` means the full-sample z was overlap |

A verdict of `UNDERPOWERED` is not a failure of the setup. It is the panel
declining to report a measurement it could not have made.
