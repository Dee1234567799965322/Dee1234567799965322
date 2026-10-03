import urllib.request, json, time, csv, sys

def fetch(gran, hours_back):
    # Coinbase: [time, low, high, open, close, volume], newest first, max 300/req
    out = {}
    end = int(time.time())
    span = 300 * gran
    start_limit = end - hours_back * 3600
    tries = 0
    while end > start_limit and tries < 400:
        start = end - span
        url = (f"https://api.exchange.coinbase.com/products/BTC-USD/candles"
               f"?granularity={gran}&start={start}&end={end}")
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "bt/1.0"})
            data = json.load(urllib.request.urlopen(req, timeout=25))
        except Exception as e:
            time.sleep(1.0); tries += 1; continue
        if not data:
            break
        for row in data:
            out[int(row[0])] = row  # dedupe by time
        oldest = min(r[0] for r in data)
        end = oldest  # step back
        tries += 1
        if tries % 10 == 0:
            print(f"  ...{len(out)} bars, at {time.strftime('%Y-%m-%d', time.gmtime(oldest))}", file=sys.stderr)
        time.sleep(0.25)
    rows = sorted(out.values(), key=lambda r: r[0])
    return rows

gran = int(sys.argv[1]) if len(sys.argv) > 1 else 3600
hours = int(sys.argv[2]) if len(sys.argv) > 2 else 8760
path = sys.argv[3] if len(sys.argv) > 3 else "/tmp/btc.csv"
print(f"fetching gran={gran}s hours_back={hours}", file=sys.stderr)
rows = fetch(gran, hours)
with open(path, "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["time", "low", "high", "open", "close", "volume"])
    for r in rows:
        w.writerow(r[:6])
print(f"saved {len(rows)} bars to {path}")
if rows:
    print("from", time.strftime('%Y-%m-%d', time.gmtime(rows[0][0])),
          "to", time.strftime('%Y-%m-%d', time.gmtime(rows[-1][0])))
