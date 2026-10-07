# Auction Cipher — User Guide

Oct 7, 2026

Part 1 explains how to use the indicator. Part 2 is the full settings reference.

# Part 1 — How to use it

## Set up in five minutes

Do these once per chart. After that, the indicator tells you where the trade locations are, when a setup is complete, and what size to trade.

1. **Add it.** Open the Pine Editor, paste the code from `AuctionCipher.pine` in your GitHub repo, click *Add to chart*. It draws on the price chart and opens one lower pane.
2. **Pick a preset.** Settings → *\* START HERE* → **Chart Preset**. Use **Clean** while trading, **Standard** while studying.
3. **Check the instrument.** Leave **Instrument Profile** on *Auto-detect* for BTC and gold. For anything else, set it to *Manual* and choose **Period Mode** in group 1.
4. **Enter your real numbers.** Group *25 - LIVE RISK*: **Account size ($)** and **Risk per trade (%)**. Start at 0.5% or less.
5. **Create one alert.** TradingView *Alert* → Condition: *Auction Cipher* → **Any alert() function call** → *Once per bar close*. Every BUY/SELL, with its size and stop, arrives through this single alert.

Best timeframes: **1h** for intraday, **4h** for swings. On 15m and below the signals did not hold up in testing (see the last section).

## Reading the chart

Three places carry everything: the **read box** at the top right of price, the **ACTION** row in the dashboard, and the **levels**. The read box and ACTION are the only two that tell you to do something; every other mark is evidence.

**The two you act on**

| Where | What it says | Meaning |
| --- | --- | --- |
| Read box, first line | BALANCE / IMBALANCE / TRANSITION + an instruction | Today's playbook (next section). |
| Read box | >>> BUY SIGNAL + Size …u @ stop … | A complete setup, with your position size and stop. |
| Dashboard ACTION | WAIT | Nothing to do. |
| Dashboard ACTION | buy setting up / sell setting up | Three gates open; the fourth is missing. Get ready, don't enter. |
| Dashboard ACTION | BUY 2.0R / SELL 2.0R | Signal live, with its reward-to-risk. |
| Dashboard ACTION | CONFLICT | Both sides qualified. Stay out. |

**Levels and marks on the price chart**

| You see | It is | Use it as |
| --- | --- | --- |
| Grey lines labelled prior POC / VAH / VAL | Yesterday's value area | The main places to look for a trade. |
| Amber line (POC), cyan lines (VAH/VAL) | Today's developing value | Targets and context. |
| Pink line nPOC | An old POC price never went back to | A magnet — likely target. |
| Green IB lines | Initial balance (opening range) | Breakout reference. |
| Orange line | VWAP | Fair price now; far from it = stretched. |
| Yellow/red lines | Weekly POC / VAH / VAL | The bigger picture's edges. |
| Green BUY / red SELL label | A full four-gate signal | Your entry (next section). |
| Red and green boxes after a signal | Stop zone and target zone | Where you are wrong, where you get paid. |
| × marked TP | Target reached | Trade done. |
| Orange square above a bar | Absorption | Someone is defending this price. |
| Yellow × | Liquidation cascade | Forced selling/buying; often overshoots, then reverses. |
| BOS / CHoCH labels | Structure break with / against trend | CHoCH = first warning the trend may turn. |
| Grey boxes with a small profile | Balance area | Its edges are trade locations; a break out of it can run. |

**The lower pane**

| You see | Meaning |
| --- | --- |
| Dark waves crossing | WaveTrend momentum. The cross is the TRIGGER. |
| Green/red area near zero | Money flow — green = buyers in control. |
| Yellow dot / white dot | Momentum cross up / down. Big dot = a divergence came with it. |
| Circle / diamond on the waves | Confirmed WaveTrend / CVD divergence (marked 5 bars back — a delay, not a repaint). |
| Faint early marker | Divergence still forming. A warning only; it can disappear. |
| Strip at the bottom | Trend ribbon: green bullish, red bearish structure. |

## Before you trade: pick the playbook

The first line of the read box decides what kind of trade you are allowed to take today. Read it before every session and only take signals that agree with it.

| Read box says | What the market is doing | Your playbook |
| --- | --- | --- |
| **BALANCE — Fade the edges back to POC** | Two-way trade inside a range | Sell near VAH, buy near VAL, target the POC. Above value → sells favoured; below value → buys favoured; mid-value → wait for an edge. |
| **BALANCE by value, but a TREND DAY is running — do NOT fade** | Range on paper, but today keeps extending | No fading. Wait for the range to stop expanding, or trade only with the direction. |
| **IMBALANCE — Go with it, do not fade** | Value is moving to a new area | Trade with the move only. Targets: the untested POC shown in the read. |
| **TRANSITION — Stand down** | The auction hasn't decided | No trade. |

The lines under the headline add detail:

- **Price is above value (expensive) / below value (cheap) / inside value** — where price sits against today's value area.
- **Zoomed out: price is …** — the same against the weekly value area. A buy into weekly value from below is stronger than one into weekly resistance.
- **High/Low is POOR** — unfinished; price usually comes back to it. Good target, bad place to fade.
- **High/Low is EXCESS** — finished; the rejection was real. Good place to lean against.
- **ABSORPTION now / EXHAUSTION now** — a live warning on the current bar.

**Pre-session checklist**

- [ ] Read the headline and note the playbook.
- [ ] Note where price sits: above, below or inside value.
- [ ] Mark the two nearest trade locations: prior VAH/VAL, nPOC, weekly edge.
- [ ] Check for a POOR high or low to use as a target.
- [ ] Decide which side you are allowed to trade. Ignore signals on the other side.

## Taking a BUY or SELL

A signal is only confirmed when its bar closes, so you enter on the **next bar's open**, never at the signal bar's close. The alert and the read box give you every number you need.

1. **The signal prints.** A green BUY or red SELL label appears, ACTION shows *BUY 2.0R* (or SELL), and the alert arrives: *CHART BUY … Entry at the NEXT bar open, stop X, target Y. Stand down if the open leaves less than 1.5R. LIVE SIZE 0.1u, wide stop Z ($50 risk).*
2. **Check the playbook.** Does it match the read box? A buy on an IMBALANCE-down day, or any signal on TRANSITION, gets skipped.
3. **Wait for the next bar to open.** If price opened so far toward the target that less than 1.5R is left (your *Minimum R*), skip it.
4. **Enter at market** with the size from the **LIVE SIZE** line.
5. **Put your stop at the wide stop price** (Z). The size was calculated for that stop, so this keeps your loss at exactly your risk amount.
6. **Put your target at the target price** (Y), the top of the green box. It is capped at 2R by default.

**Worked example (BTC):** account $10,000, risk 0.5% = $50. Entry 60,000, wide stop 59,500 → distance $500 → size $50 ÷ $500 = **0.1 BTC**. If the stop is hit you lose $50, whatever the distance.

Two stops are shown on purpose. The **red box** is the tighter structural stop that the statistics measure. The **wide stop** sits 0.5× ATR beyond it so normal noise doesn't tag you out. Trade the wide stop together with the size printed next to it. For futures, the size is in ounces or coins, so divide by the contract size (GC = 100 oz, MGC = 10 oz).

## Managing and exiting the trade

Once you're in, the plan is fixed: leave the stop and target alone and let one of three things end the trade.

| What happens | On the chart | What you do |
| --- | --- | --- |
| Target reached | × marked **TP** | Take the profit at the target. Don't hold for more — in testing, trades that ran past 2R usually gave it back. |
| Stop reached | Price trades through the stop | Accept the loss. It is the planned risk amount, nothing more. |
| A full opposite signal appears | SELL while you're long (or BUY while short) | Close at market. The reason for the trade is gone. Go flat; don't flip into the new direction. |

Rules while a trade is open:

- **Don't tighten the stop.** In the backtest, stops tighter than about 1.5× ATR never reduced losses; they only got hit more often.
- **No new signal will show** while a trade is open (*One Trade At A Time* is on). That is deliberate.
- **Track it live** in the statistics table: the *Open now (live R)* row shows how far in profit or loss the open trade is, in R.
- **CHoCH or absorption against you** near the target is a reason to take profit early, not to add to the position.

## Check it works before you risk money

Auction Cipher shows you where a trade makes sense; it does not guarantee the trade wins. Our testing over the past month never proved a reliable edge. On 15m no stop setting was profitable, and on 1h the best result was a thin +$331 over 71 trades. Prove it on your own market first.

**Test it on your symbol and timeframe**

1. Load as much history as TradingView allows on the chart you plan to trade.
2. Set **Slippage (ticks)** in group 21 to what your exchange really costs you.
3. Read the statistics table: **Expectancy R/trade** must be above 0, and the trade count should be at least 20 — 100+ is better. Check the *Verdict (drift-controlled)* row too.
4. Paper trade the steps above for 2–4 weeks, or about 20 trades, before using real money.
5. Change **one setting at a time**, then re-read the statistics. Never change settings because of one loss.

**Rules that protect the account** (suggested limits — adjust to your situation)

- Risk 0.5% or less per trade. Size always comes from the LIVE SIZE line, never by feel.
- Stop for the day after 2 losses in a row, or once the day is down 1.5%.
- One trade at a time. No revenge trades and no adding to a loser.
- No signal that disagrees with the read box. TRANSITION means no trades.
- Keep a simple log: date, signal, entry, stop, exit, R. After 20 trades, compare your R to the statistics table.

# Part 2 — Settings reference

## How to use this guide

Open the settings at the top group, **\* START HERE - CHART PRESET**: the Chart Preset there overrides most on/off switches in the rest of the menu. If you flip a toggle and nothing changes on the chart, this is why — set Chart Preset to **Custom (use the groups below)** first.

The settings groups are numbered in the menu. This guide follows them in the order they matter for trading, not menu order. Each section lists the settings worth knowing, their default, and when to change them; pure colour pickers are left out unless they matter.

**The five settings to check first:**

1. **Chart Preset** (\* START HERE) — Clean, Standard, Everything, or Custom.
2. **Instrument Profile** (\* START HERE) — leave on Auto-detect for BTC and gold.
3. **Period Mode** (1 - PERIOD) — only matters if Instrument Profile is Manual or the symbol isn't BTC/gold.
4. **Gate Mode** and **Sensitivity** (16 - CHART SIGNALS) — decide how strict BUY/SELL signals are.
5. **Account size** and **Risk per trade** (25 - LIVE RISK) — set these to your real account before reading the size in the signal pop-up.

## Presets and instrument profile

**Chart Preset** (default Standard) decides which layers draw. The table shows what each preset actually turns on in the code. Anything not listed here is controlled by its own group's toggle.

| Layer | Clean | Standard | Everything |
| --- | --- | --- | --- |
| Auction layer, prior POC/VAH/VAL, naked POCs | on | on | on |
| VWAP line | on | on | on |
| Chart BUY/SELL signals, risk layer, CME gap | on | on | on |
| Profile histogram, initial balance, low volume nodes | off | on | on |
| VWAP bands, golden pocket fibs | off | on | on |
| Volume DNA, DNA glow, absorption clouds | off | on | on |
| Market structure, balance areas, OI, liquidation cascades, statistics | off | on | on |
| Prior high/low, DNA circles, DNA tape, volume bubbles, fib targets, session boxes | off | off | on |

Use **Clean** for live trading, **Standard** for daily analysis, **Everything** only for studying. Pick **Custom** to control every layer yourself with the toggles in each group.

**Instrument Profile** (default Auto-detect) reads the ticker and switches only the settings that genuinely differ by instrument. The menu still shows your typed values; the script runs on these instead:

| Setting | BTC / crypto | Gold futures (GC) | Spot gold (XAUUSD) |
| --- | --- | --- | --- |
| Period Mode | 24h UTC | RTH Session 08:20–13:30 New York | Chart Daily |
| Initial Balance | 240 min | 60 min | 240 min |
| CME gap symbol | CME:BTC1! | COMEX:GC1! | COMEX:GC1! |

Set it to **Manual** only for other symbols (ES, NQ, stocks, FX); then group 1 and group 20 settings apply exactly as typed.

**0 - LABELS** controls the text next to each line: Name Every Line (on), Label Content (Name + Price), Label Size (Small), and Show Plain-English Read (on). If labels overlap, raise *Gap Between Side-by-side Labels* (14) or *Label Collision Tolerance* (0.5× ATR).

## Auction core — groups 1, 2 and 2b

These build the volume profile: POC, value area (VAH/VAL), prior levels, naked POCs and low volume nodes. Defaults are sound; the two you may touch are **Profile Rows** (if the script feels slow) and **Profile Range**.

**1 - PERIOD**

| Setting | Default | What it does / when to change |
| --- | --- | --- |
| Period Mode | 24h UTC (crypto) | When a new profile starts. Overridden by Instrument Profile unless that is Manual. RTH Session for CME futures, Weekly for a composite. |
| RTH Session / RTH Session Timezone | 08:20–13:30, New York | Used only in RTH Session mode. Not the same as the Session Ranges timezone in group 22. |
| Initial Balance (minutes) | 240 | Opening range length. 60 for a futures pit session; 240 is the same fraction of a 24h crypto day. |

**2 - AUCTION LAYER**

| Setting | Default | What it does / when to change |
| --- | --- | --- |
| Enable Auction Layer | on | Master switch for the profile and its levels. |
| Profile Rows | 250 | Price precision of POC and value area. Lower to 100–150 if the chart lags. |
| Value Area % | 70 | Share of volume inside VAH–VAL. 70 is standard; leave it. |
| Profile Range | Auction Period | Auction Period = fixed levels for the session. Rolling Lookback = profile follows price (last N bars). |
| Rolling Lookback (bars) | 300 | Only used with Rolling Lookback. Max 480. |
| Profile Histogram | on | Draws the profile shape on the right. |
| Histogram Width (%) | 34 | Width of the widest row as % of period bars. |
| Split Up / Down Volume | on | Coloured overlay per row: green = buyers dominated that price, red = sellers. |
| Extend To The Right / Histogram Offset | on / 8 bars | Where the histogram sits. Raise offset if it crowds price. |
| Prior POC / VAH / VAL | on | Yesterday's value levels — the main trade locations. |
| Prior High / Low | off | Previous period extremes. |
| Initial Balance Lines | on | IB high/low for the current period. |
| Naked (untested) POCs / Max / Ignore Beyond | on / 12 / 15% | Old POCs price hasn't revisited; removed once touched. |
| Low Volume Nodes / Threshold / Max | on / 20% of POC / 6 | Thin shelves where price tends to move fast. |
| Excess / Poor bar counts / Extreme band | 1 / 3 / range ÷ 24 | Classifies the period's high and low as EXCESS (rejected) or POOR (likely revisited). Rarely needs changing. |

**2b - AUCTION COLORS** holds the colours for the histogram, POC (amber), VAH/VAL (cyan), prior value (grey), naked POCs (pink), LVNs (purple) and IB (green).

## Volume DNA and Volume Bubbles — groups 11, 11b and 12

Volume DNA labels each bar by effort (volume) versus result (bar size). **Absorption — high volume, narrow bar — is the one to watch**, especially at VAH/VAL; it also feeds the PROOF gate of the BUY/SELL signals.

| DNA state | Volume | Bar spread | Meaning | Default colour |
| --- | --- | --- | --- | --- |
| Absorption | high | narrow | Someone is soaking up all orders | orange |
| Effort | high | wide | Participation and follow-through agree | cyan (up) / pink (down) |
| Exhaustion | low | wide | Move running on empty | yellow |
| Stagnation | low | narrow | Nobody trading | grey (off by default) |

**11 - VOLUME DNA**

| Setting | Default | What it does / when to change |
| --- | --- | --- |
| Enable Volume DNA | on | Master switch. |
| Volume / Spread Lookback | 20 / 20 | Bars used to judge "normal" volume and bar size. |
| Volume Std Dev Threshold | 1.5 | How unusual volume must be. Raise to 2.0 for fewer, stronger marks. |
| Spread Std Dev Threshold | 1.0 | How unusual bar size must be. |
| Mark Absorption / Effort / Exhaustion / Stagnation | on / on / on / off | Which states get marked. |
| Only Mark at Value Area Edges | off | Turn on to keep only DNA marks at VAH/VAL — cuts noise a lot. |

**11b - VOLUME DNA - VISUALS**

| Setting | Default | What it does |
| --- | --- | --- |
| Ghost Glow Candles | on | Coloured halo around DNA bars. |
| Absorption Clouds / Cloud Extension | on / 10 bars | Orange zone projected forward from absorption, labelled with volume. |
| DNA Circles with Volume | off | Circle per DNA bar, sized by how extreme volume was. |
| Barcode Heatmap Tape / Rows / Position | off / 20 / Middle Right | Strip showing the DNA state of the last N bars. Keep it away from the dashboard position. |

**12 - VOLUME BUBBLES** (off by default; on in the Everything preset) marks unusually large volume clusters as Small/Medium/Big bubbles.

| Setting | Default | What it does |
| --- | --- | --- |
| Detection Method | Volume OR Delta | What counts as "big". Volume + Delta is strictest. |
| Buy/Sell Classification | Both | Colours bubbles by candle direction, delta, or both agreeing. |
| Small / Medium / Big Percentile | 75 / 90 / 97 | Size thresholds. Raise Small to 85 to show fewer bubbles. |
| Consensus Mode | Majority (2 of 3) | Must be big on 2 of the 3 windows (20/50/100 bars). |
| Show Numbers / Bubble Text | on / Volume | Text inside each bubble. |

## Higher-timeframe value, HTF candles, VWAP and fibs — groups 18, 18b, 13 and 14

These add slower reference levels around the session profile. The weekly value area (on by default) is the one that matters most: it tells you whether today's value sits high or low in the bigger auction.

**18 - HIGHER TIMEFRAME VALUE**

| Setting | Default | What it does / when to change |
| --- | --- | --- |
| HTF Value Area | Weekly | A second, slower profile: Off, Daily, Weekly, Monthly. Use Daily on 1–5m charts, Monthly on 4h+. Its last completed VAH/VAL also count as signal locations. |
| HTF POC / HTF VAH/VAL colours | yellow / red | Line colours. |

**18b - HTF CANDLES** (off by default)

| Setting | Default | What it does |
| --- | --- | --- |
| Show HTF Candles | off | Draws higher-timeframe candles beside the chart, live candle included. No data request, never repaints. |
| Candle Timeframe | 240 (4h) | Must be higher than the chart timeframe. |
| Candles Shown / Offset / Width / Gap | 4 / 60 / 5 / 4 bars | Layout. Raise Offset if it overlaps the profile. |
| Extend Open/High/Low of the Live Candle | on | Rays from where the HTF open/high/low were actually made. |
| Label the Live Candle | on | Timeframe, % change, and where the close sits in its range (0% = low, 100% = high). |

**13 - VWAP**

| Setting | Default | What it does / when to change |
| --- | --- | --- |
| Show VWAP | on | Volume-weighted average price. When VWAP and POC sit apart, value is still moving. |
| VWAP Anchor | Auction Period | Keeps VWAP on the same clock as the profile. Daily / Weekly / Session also available. |
| Show Std Dev Bands / Band 1 / Band 2 | on / 1.0 / 2.0 | Deviation bands. Band 1 can be used as a signal location (see group 16). |

**14 - FIB LEVELS**

| Setting | Default | What it does / when to change |
| --- | --- | --- |
| Golden Pockets (retracement) | on | 0.5 / 0.618 / 0.786 / 0.886 of the latest swing. |
| Swing Window (bars) | 120 | Swing must be inside this window or fibs aren't drawn. |
| Minimum Leg Length (bars) | 15 | Ignores tiny swings. |
| Count the Golden Pocket as Confluence | off | Adds 0.618 and 0.786 to the signal confluence count. Off on purpose — it changes how many signals fire. |
| Custom Target Fibs (extension) | off | 1.47 / 1.55 / 2.56 / 2.60 / 2.64 targets. Targets, not entries. |
| Hide Fibs Beyond (% from price) | 25 | Stops far-away extensions from squashing the price scale. |

## Oscillator pane — groups 3 to 8, 27 and the lower-pane visuals

The lower pane is the Market Cipher B-style momentum view. WaveTrend crosses here are the TRIGGER for chart signals; divergences are the main PROOF. Leave the WaveTrend lengths alone — every threshold in the script is tuned to them.

**3 - MOMENTUM WAVES (WaveTrend)**

| Setting | Default | What it does |
| --- | --- | --- |
| Channel / Average / Signal Length | 9 / 12 / 3 | The WaveTrend formula. Don't change. |
| Overbought 1 / 2 | 53 / 60 | Extreme zones. A cross beyond ±53 counts as "in the zone". |
| Oversold 1 / 2 | −53 / −60 | Same, downside. |

**4 - MONEY FLOW**

| Setting | Default | What it does / when to change |
| --- | --- | --- |
| Source | Volume Delta (intrabar) | Real buy-minus-sell volume. Most informative. Alternatives: Money Flow Index, Chaikin, or the OG Market Cipher formula (contains no volume). |
| Show Money Flow / Length / Smoothing | on / 60 / 3 | The green/red area. |
| Auto-normalise Height / Height | on / 1.0 | Keeps the area a readable size whichever source you pick. |

**5 - VWAP WAVE**: Show VWAP Wave (on), VWAP Height (1.0) — the gap between the two WaveTrend lines.

**6 - HIDDEN LINES**: Show RSI (off), RSI Length (14).

**7 - CVD**: Show CVD Line (on), CVD Anchor (Daily — also Weekly, Session, None/rolling), Rolling Length (200).

**8 - DIVERGENCES**

| Setting | Default | What it does / when to change |
| --- | --- | --- |
| WaveTrend Divergences / CVD Divergences | on / on | Which oscillators are checked. CVD divergence = sellers pressing but not being paid. |
| Draw Divergence Lines / Max Lines Kept | on / 20 | Lines on the pane. |
| Show Hidden Divergences | off | Continuation divergences, drawn as X marks. |
| Hidden Divergence Counts as Proof | off | Lets hidden divergences produce signals. Measure before using. |
| Pivot Left / Right Bars | 5 / 5 | Right bars = confirmation delay. Markers appear 5 bars back — a delay, not a repaint. |
| Min / Max Bars Between Pivots | 5 / 60 | Range of swing spacing that counts. |
| Minimum Divergence Quality (0–4) | 0 | 0 = off. Raise to 1–2 only after comparing expectancy in the statistics table. |
| Quality checks | Participation on, OI on, At A Real Level on, Correlated Market off | Each scores one point. Correlated Market needs a symbol (gold: TVC:DXY, Inverse on; BTC: BINANCE:ETHUSDT.P, Inverse off). |

**27 - FORMING DIVERGENCE** shows a divergence while it is still forming, before the pivot confirms — an early warning only, never a signal. Defaults: on, Only in the Extreme Zone on, Only at an Auction Level on. It can disappear if price keeps going.

**MARKET CIPHER B: VISUALS (LOWER PANE)** holds the wave, money-flow and dot colours, the trend ribbon (on, between −95 and −105), and **MCB Dots Filter** (None) — set it to *Extreme Waves + Money Flow* to show only the higher-quality cross dots.

## Market structure, balance areas, CME gap and sessions — groups 15, 19, 20 and 22

These draw context on the price chart. Balance-area edges also act as signal locations; the other three are visual only.

**15 - MARKET STRUCTURE**

| Setting | Default | What it does / when to change |
| --- | --- | --- |
| Show Structure (BOS / CHoCH) | on | BOS = break with the trend (continuation). CHoCH = break against it (first warning of a turn). |
| Swing Strength | 10 | Bars each side to confirm a swing. Lower (5) for scalping, higher (15–20) for swings. |
| Label Swings (HH/HL/LH/LL) | on | Swing tags. |
| Max Structure Marks | 12 | Older marks are deleted past this. |

**19 - BALANCE AREAS** finds ranges by volatility contraction (ADX falling) rather than by the clock, then profiles them.

| Setting | Default | What it does / when to change |
| --- | --- | --- |
| Detect Balance Areas | on | Master switch. |
| ADX Length / ADX Threshold | 14 / 30 | ADX falling through 30 opens a box. Higher threshold = only deep contractions. |
| Build Length (bars) | 20 | How long the box grows before it is armed for a break. |
| Balance Profile Bins / Draw Balance Profile | 20 / on | The mini-profile inside the box. |
| Use Balance Edges as Signal Location | on | Box high/low count as valid BUY/SELL locations. |

**20 - CME GAP**

| Setting | Default | What it does |
| --- | --- | --- |
| Show CME Gaps | on | Untraded weekend range on CME futures, drawn as a box until filled. |
| CME Symbol | CME:BTC1! | Auto-switched by Instrument Profile (gold uses COMEX:GC1!). |
| Weekend Gaps Only | on | Ignores ordinary daily-open gaps. Leave on. |
| Minimum Gap (%) / Max Open Gaps | 0.5 / 6 | Gold auto-uses a smaller minimum. |

**22 - SESSION RANGES** (on only in the Everything preset or Custom)

| Setting | Default | What it does |
| --- | --- | --- |
| Show Session Ranges | on | Asia / London / New York boxes. |
| Asia / London / New York | 00:00–08:00 / 08:00–16:00 / 13:00–21:00 | Session windows. |
| Session Range Timezone | UTC | Timezone for these boxes only — not the RTH timezone in group 1. |
| Days To Keep / Label Sessions | 3 / on | History and labels. |

## Chart BUY/SELL signals — group 16

A BUY or SELL appears on the price chart only when four layers agree, then survives a set of filters. Pane dots need momentum alone; chart signals need all of this:

1. **CONTEXT** — the regime allows the direction (no buys while value is migrating down, when Require Regime Agreement is on).
2. **LOCATION** — price touched a level and closed back: prior VAH/VAL, naked POC, initial balance, prior high/low, VWAP ±1 band, weekly VAH/VAL, balance edges.
3. **TRIGGER** — a WaveTrend cross.
4. **PROOF** — a divergence, absorption, money flow crossing zero, OI flush, or delta divergence (whichever are switched on).
5. **Filters** — dropped if both sides qualify at once, if efficiency is too low (when on), if open interest shows real positioning against it, if the target is under the Minimum R, or if a trade is still open.

**Gate Mode** is the biggest switch. The code default is **Window (legacy)**: each gate only has to have happened within the last 8 bars. **Same event (strict)** requires a divergence, with the rejection and the cross belonging to that same swing — far fewer signals.

| Setting | Default | What it does / when to change |
| --- | --- | --- |
| Show Buy / Sell on Price Chart | on | Master switch. |
| Gate Mode | Window (legacy) | See above. |
| Event Tolerance (bars) | 4 | Same event mode only: how far the rejection and cross may sit from the divergence pivot. |
| Sensitivity | Strict (all 4) | Window mode only. Standard = 3 of 4, Loose = location + trigger, Wave only = trigger alone (for testing). Seeing no signals on Window? Turn this first. |
| Cross Must Be In Extreme Zone | off | On = only crosses beyond ±53. Can mean days with no signal in a range. |
| Rejection Must Close In Direction | off | On = also needs an up candle for a buy. Usually leave off. |
| Count VWAP Bands as Location | on | VWAP ±1 band counts as a level. |
| Cooldown (bars between signals) | 20 | Minimum gap before the same side signals again. |
| Trigger Window (bars) | 3 | How far apart cross and touch may be (Window mode). |
| Location Tolerance (%) | 0.12 | How close a wick must come to a level. Lower it if confluence is always high. |
| One Trade At A Time | on | No new signal while one is open. |
| Opposite Signal Closes Open Trade | on | A full opposite setup closes the trade (flat, not reversed). |
| Reversal Close Trigger | Opposite setup completes | Alternative: also needs the opposite momentum cross. |
| Minimum Level Confluence | 1 | Levels that must stack at the rejection price. 2–3 = only strong clusters, far fewer signals. |
| Require Efficient Price Movement / Lookback / Minimum | off / 20 / 0.25 | Noise filter. Trends run 0.3–0.6; chop is under 0.15. |
| Require Regime Agreement | on | Stops you fading a trend day. Leave on. |
| Regime Confirmation (closes) | 3 | Closes beyond prior value before a trend is recognised. |
| Buy / Sell Color | green / red | Signal colours. |

## Risk layer and Live Risk sizing — groups 21 and 25

The risk layer draws a structural stop and a target for every signal; Live Risk turns that stop into a position size in the BUY/SELL pop-up and alert. **Set Account size and Risk per trade to your real numbers before trading off the pop-up.**

**21 - RISK LAYER**

| Setting | Default | What it does / when to change |
| --- | --- | --- |
| Draw Stop / Target / R | on | Stop and target boxes. Turning it off hides the boxes only; the filter still works. |
| Stop Buffer (× ATR) | 0.3 | Extra room below the swing low (above the swing high for shorts). |
| Stop Swing Lookback | 5 | Bars searched for the swing the stop sits behind. |
| Minimum Stop Distance (× ATR) | 0.6 | The stop is never closer than this. See the backtest note below. |
| Minimum R to Show Signal | 1.5 | Signals with target closer than 1.5× the risk are hidden. |
| Cap Target at (R) | 2.0 | Target capped at 2R. Keep it above Minimum R. 0 = no cap. |
| Assumed Fill | Next bar open (realistic) | Where the statistics assume you got in. Leave it. |
| Slippage (ticks) | 0 | Set to your venue's real cost so expectancy is honest. |
| Box Extend (bars) | 25 | Box length. |

**25 - LIVE RISK (position size)**

| Setting | Default | What it does |
| --- | --- | --- |
| Show size in signal pop-up / alert | on | Adds a size line to the BUY/SELL pop-up and alert. |
| Account size ($) | 10,000 | Your account. |
| Risk per trade (% of account) | 0.5 | Dollars lost if the stop is hit. 0.5% of $10,000 = $50. |
| Widen stop past structure (× ATR) | 0.5 | Pushes the stop past noise; size shrinks so dollar risk stays the same. |

Size = risk dollars ÷ distance from entry to the widened stop. Example: $50 risk with a $500 stop distance on BTC = 0.1 BTC. The size is in **units of the underlying** (BTC, ounces), not contracts. For futures, divide by the contract size — GC is 100 oz, MGC is 10 oz.

**Stop-loss backtest (BTC, Coinbase data).** Sweeping *Minimum Stop Distance* from 0.25 to 6× ATR at fixed dollar risk:

- Below about 1.5× ATR the setting changes nothing — the swing-based stop is already wider.
- On **1h**, the best result was at **2.5× ATR** (28% win rate, 2.96 payoff, +$331 over 71 trades); 1.5–2× and 3.5×+ were worse.
- On **15m**, no stop width was profitable.

So a tighter stop does not lower losses here. If you trade 1h, try **2.0–2.5** instead of 0.6. Treat it as a starting point, not proof: 71 trades is a thin sample that only just covers fees.

## Open interest and order flow — groups 17 and 24

Open interest (perps only) tells you who is moving price; the order flow engine reads intrabar buying and selling. Both can feed the signal gates, but only OI is wired in by default.

| Price | Open interest | Meaning |
| --- | --- | --- |
| Up | Up | New longs — real buying |
| Up | Down | Shorts covering — a squeeze, tends to stall |
| Down | Up | New shorts — real selling |
| Down | Down | Longs closing or liquidated — a flush |

**17 - OPEN INTEREST & FUNDING**

| Setting | Default | What it does / when to change |
| --- | --- | --- |
| Enable Open Interest | on | Needs an OI feed (e.g. Binance BTC perp). Spot gold shows "no OI feed", which is correct. |
| Mark Liquidation Cascades | on | Yellow × on a wide bar where OI collapses — forced closing that often overshoots. |
| Count OI as Signal Proof | on | A flush into support (or a squeeze into resistance) counts as PROOF. |
| Veto Signals Against Real Positioning | on | Blocks a sell into rising price on rising OI, and a buy into falling price on rising OI. Keep on. |
| Liquidation OI Drop / Spread (std dev) | 1.5 / 1.2 | How extreme a bar must be to count as a cascade. |
| Funding Symbol (optional) | blank | Leave blank unless you know your venue's funding ticker. |

**24 - ORDER FLOW** runs a footprint engine without drawing the grid. It changes no signal until you turn on one of the last three options.

| Setting | Default | What it does / when to change |
| --- | --- | --- |
| Enable Order Flow Engine | on | Reads buy/sell volume inside each bar. |
| Rows per Bar | 14 | Slices per bar. More rows = finer, more levels. |
| Absorption Heavy Row Multiple | 2.5 | How much more than an average row a price must trade to count as defended. |
| Absorption Edge Band (%) | 30 | Only the top/bottom 30% of a bar counts. |
| Bars to Confirm / Levels Kept | 3 / 6 | An absorption level must hold 3 bars; it is deleted when price closes through it. |
| Delta Divergence Needs (% of volume) | 10 | Bar closes up on net selling (or the reverse) by at least this share. |
| Draw Absorption Levels | off | Draws the confirmed levels (orange lines). |
| Count Absorption as Signal Location | off | Confirmed absorption levels act as LOCATION. |
| Count Absorption in Confluence | off | Adds them to the confluence count. |
| Count Delta Divergence as Proof | off | Hidden strength/weakness counts as PROOF. |

The last three are off on purpose: each one changes how many signals fire. Turn one on at a time and compare the statistics table before and after.

## Dashboards, statistics and alerts — groups 10, 23 and 26

Three tables report on the chart. The main dashboard is for trading; the statistics and gate audit tables are for checking whether the signals actually work on your symbol and timeframe.

**10 - DASHBOARD** — Show Dashboard (on), Position (Top Right). Rows to read first:

| Row | What it tells you |
| --- | --- |
| ACTION (top right) | What to do now: BUY, SELL, wait, or conflicting evidence. |
| Regime / Day type / Open | Balance or imbalance, and how the session opened. |
| Position / Vs prior | Where price sits against value, and today's value vs yesterday's. |
| POC / VAH / VAL / nPOC up/dn | Current levels and nearest untested POCs. |
| High / Low | EXCESS or POOR extremes for the period. |
| DNA / Vol z | Current bar's Volume DNA state and how unusual its volume is. |
| Open int / OI z / Funding | Positioning read (perps only). |
| Buy gates / Sell gates | Which of the four gates are open right now, plus the live confluence count. |
| Balance area / ADX / Eff | Balance-box state and trend strength / efficiency. |
| Profile / Order flow | Which data the profile is built from, and the order-flow read. |

**23 - STATISTICS** — Show Statistics Table (on in Standard), Outcome Horizon (200 bars), Table Position (Bottom Left). It counts every past signal on the loaded chart: win/loss/expired, hit rate, **Expectancy R per trade**, and drift-controlled long/short results. Ignore any number with fewer than about 20 trades. Expectancy above 0 after slippage is the only number that matters.

**26 - GATE AUDIT** — Show Gate Audit (off), Position (Middle Left). It shows how often each gate is open across the chart. If "ALL FOUR open" is high, the cooldown — not the logic — is choosing trades. Turn it on when tuning group 16.

**Alerts.** Create one TradingView alert on this indicator with the condition **Any alert() function call**. Every event then arrives through it once per bar close: CHART BUY/SELL (with the Live Risk size and stop), Grade A/B pane signals, acceptance above/below value, CVD absorption, DNA absorption/exhaustion, balance breaks, liquidation cascades and structure breaks. Forming divergences have their own two separate alert conditions.

## Recommended setups and troubleshooting

Start from one of these and change only what the table lists. They are starting points, not proven edges: the BTC backtest found no profitable stop setting on 15m, and only a thin positive result on 1h.

| Setting (group) | Scalping 5–15m | Intraday 1h | Swing 4h and up |
| --- | --- | --- | --- |
| Chart Preset (\*) | Clean | Standard | Standard |
| HTF Value Area (18) | Daily | Weekly | Monthly |
| Swing Strength (15) | 5 | 10 | 15–20 |
| Sensitivity (16, Window mode) | Standard (3 of 4) | Strict (all 4) | Strict (all 4) |
| Cooldown (16) | 10 | 20 | 20 |
| Minimum Stop Distance (21) | 1.0 | 2.0–2.5 | 2.0 |
| Risk per trade (25) | 0.25% | 0.5% | 0.5% |
| Widen stop past structure (25) | 0.5 | 0.5 | 0.5 |

**Troubleshooting**

| Problem | Fix |
| --- | --- |
| A toggle does nothing | Set Chart Preset to Custom. |
| Sensitivity does nothing | It only works with Gate Mode = Window. Its tooltip says Same event is the default, but the real default is Window (legacy). |
| No BUY/SELL for days | Sensitivity → Standard (3 of 4); Cross Must Be In Extreme Zone off; Minimum Level Confluence 1; Minimum R → 1.2. |
| Too many signals | Minimum Level Confluence 2; Require Efficient Price Movement on; or Gate Mode → Same event. |
| Chart slow or "heavy" | Profile Rows → 100–150; turn off Volume Bubbles, DNA tape and DNA circles. |
| Profile frozen on spot gold | Instrument Profile → Auto-detect (uses Chart Daily for spot gold). |
| "no OI feed" in the dashboard | Normal on spot and stocks; OI needs a perp or futures feed. |
| Labels overlap | Raise Gap Between Side-by-side Labels or Label Collision Tolerance (group 0). |
| Pop-up size looks wrong on futures | Size is in ounces/coins; divide by the contract size. |
| "Too many tokens" after editing the code | The script sits at TradingView's 100,256-token limit. Any added feature needs something removed. |
