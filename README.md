# Auction Cipher — an indicator, and nine attempts to find an edge in it

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

## The ten corrections

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

Four of the ten are about the *denominator* — what a number is compared
against, and how many chances it had. Two are about what counts as one
observation. **None is about trading logic.** Every result this repo lost, it
lost to measurement.

---

## The files

### Kept

| File | What it is |
|---|---|
| `EdgeLab.pine` | The harness above. Six setup buckets, each against its own mirror, with all ten corrections enforced |
| `AuctionCipher.pine` | The original v3.0 indicator, 5,606 lines. A good chart tool. Audited clean; its R accounting reconciles by construction |
| `AuctionFootprint.pine` | Companion footprint/volume-profile renderer |

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
