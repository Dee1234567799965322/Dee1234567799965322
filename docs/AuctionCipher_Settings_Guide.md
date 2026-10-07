# Auction Cipher — Settings Menu Guide

Oct 7, 2026 · @Zahin Farhat

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
