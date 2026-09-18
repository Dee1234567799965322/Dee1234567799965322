# Live forward run — pre-registered protocol

Written before the first trade. The point of writing it first is correction 8:
a rule that picks its own configuration after seeing results is not a test.

---

## What this run can and cannot answer

**It cannot tell you whether there is an edge.** At this project's own power
figures, a 6.4pp effect needs roughly **1,600 trades** to be found even half the
time. At about one signal a day on the configuration below, that is six years.
No live run of a realistic length will settle the question, and any conclusion
drawn from forty trades about profitability is noise wearing a verdict's
clothes.

**It can answer four things, and they are worth answering:**

1. Do live fills match the next-bar-open assumption every backtest number rests on?
2. Is the real round-trip cost near the **0.035R** the record assumes for gold CFD?
3. Does the alert → execution loop actually work, unattended?
4. Does the panel's live-R agree with the broker's?

If any of those four comes back wrong, every number in the measurement log is
wrong too, and that is a finding worth more than the P&L.

---

## Configuration — fixed now, not adjustable mid-run

| Setting | Value | Why this, chosen before looking at performance |
|---|---|---|
| Instrument | **XAUUSD** spot CFD | Lowest measured round-trip cost of the venues tested: **0.035R** against 0.16R on a Binance perp. Cost is knowable in advance; performance is not. |
| Timeframe | **1 hour** | Mid-ladder. About one signal a day, so the log fills at a readable rate, and a 200-bar horizon is ~8 days — long enough that 0.035R is small against a 1R stop. **Not** chosen for its measured edge. |
| Gate Mode | Window (legacy) | The strict rebuild lost to it and starved the sample to 32 trades. |
| Cap Target | 2.0R | The value the entire record was measured on. |
| Outcome Horizon | 200 bars | Default; changing it changes what every published figure means. |
| Fill | Next bar open (realistic) | The assumption under test. |
| Opposite Signal Closes Trade | ON | As measured. |

Load the build whose panel header reads **`r18`**. Reset settings to defaults
first, then set the above — adding inputs shifts TradingView's saved-value
mapping and a field can silently keep an old value.

---

## Size

| | |
|---|---|
| Risk per trade | **0.25% of account** |
| Hard stop for the whole run | **−15R cumulative** ≈ −3.75% of account |
| Review point | **40 closed trades** |

Pick the account size such that losing 3.75% of it would not change a single
decision you make that month. If no such size exists, the right size is zero.

---

## Alerts

Create Alert → Condition: **Auction Cipher v3.0** → **Any alert() function call**
→ **Once Per Bar Close**. Every event the script raises comes through that one
alert; nothing else needs configuring.

Once per bar close is not optional. Intrabar alerts fire on prices that can be
revised before the bar finishes, and the entire record is measured on confirmed
bars.

---

## What to record, per trade

Date · direction · signal price · fill price · stop · target · exit · realised R

The fill-versus-signal gap is the column that matters. The panel assumes you
got the next bar's open; this column is where you find out.

---

## Stopping rules — any one of these ends the run

1. Cumulative **−15R**.
2. **40 closed trades** reached → stop and review before continuing.
3. Realised cost per trade above **0.08R** — double the assumption. The venue is
   wrong and every cost figure in the record needs redoing.
4. Panel R and broker R disagree by more than **10%** on any trade. The
   measurement is broken; fix it before generating more numbers with it.

Rules 3 and 4 are more important than rule 1. A losing run tells you little at
this sample size. A **measurement** that disagrees with reality invalidates
twenty thousand trades of prior work, and this is the cheapest opportunity to
catch it.

---

## What the record says you should expect

Across twelve bar sizes and two instruments, 4,135 resolved trades, the
drift-controlled edge averages **−0.15pp** and not one of twenty-one cells
reaches |z| 1.96. Expectancy per configuration sits between −0.05R and +0.03R.

**The honest prior for this run is break-even minus costs.** Forty trades at
0.25% risk is an expected outcome indistinguishable from zero, with a spread of
several R either way. Go in expecting to learn about execution, not about edge.
