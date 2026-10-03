import csv, sys, math
VERBOSE=False

def load(path):
    o=[];h=[];l=[];c=[];v=[];t=[]
    with open(path) as f:
        r=csv.reader(f); next(r)
        for row in r:
            t.append(int(row[0])); l.append(float(row[1])); h.append(float(row[2]))
            o.append(float(row[3])); c.append(float(row[4])); v.append(float(row[5]))
    return t,o,h,l,c,v

def ema(src,n):
    out=[None]*len(src); k=2/(n+1); e=None
    for i,x in enumerate(src):
        e=x if e is None else x*k+e*(1-k); out[i]=e
    return out
def sma(src,n):
    import collections; out=[None]*len(src); s=0; dq=collections.deque()
    for i,x in enumerate(src):
        x=0 if x is None else x; dq.append(x); s+=x
        if len(dq)>n: s-=dq.popleft()
        out[i]=s/len(dq)
    return out
def atr(h,l,c,n=14):
    tr=[0.0]*len(c)
    for i in range(len(c)):
        tr[i]=h[i]-l[i] if i==0 else max(h[i]-l[i],abs(h[i]-c[i-1]),abs(l[i]-c[i-1]))
    return ema(tr,n)

def mfi(h,l,c,v,n=14):
    tp=[(h[i]+l[i]+c[i])/3 for i in range(len(c))]
    pos=[0.0]*len(c); neg=[0.0]*len(c)
    for i in range(1,len(c)):
        rmf=tp[i]*v[i]
        if tp[i]>tp[i-1]: pos[i]=rmf
        elif tp[i]<tp[i-1]: neg[i]=rmf
    out=[None]*len(c)
    import collections; dp=collections.deque(); dn=collections.deque(); sp=0; sn=0
    for i in range(len(c)):
        dp.append(pos[i]); sp+=pos[i]; dn.append(neg[i]); sn+=neg[i]
        if len(dp)>n: sp-=dp.popleft(); sn-=dn.popleft()
        out[i]=100 - 100/(1+(sp/sn)) if sn>0 else (100.0 if sp>0 else 50.0)
    return out

def profile(hs,ls,vs,rows,pct):
    if not hs: return None
    hi=max(hs); lo=min(ls); rng=hi-lo
    if rng<=0: return None
    step=rng/rows; bins=[0.0]*rows
    for j in range(len(hs)):
        bv=vs[j]
        if bv<=0: continue
        a=max(0,min(rows-1,int((ls[j]-lo)/step))); b=max(0,min(rows-1,int((hs[j]-lo)/step)))
        sl=bv/(b-a+1)
        for k in range(a,b+1): bins[k]+=sl
    tot=sum(bins)
    if tot<=0: return None
    poc=bins.index(max(bins)); target=tot*pct; acc=bins[poc]; up=poc+1; dn=poc-1
    while acc<target and (up<=rows-1 or dn>=0):
        vu=bins[up] if up<=rows-1 else -1; vd=bins[dn] if dn>=0 else -1
        if vu<0 and vd<0: break
        if vu>=vd: acc+=vu; up+=1
        else: acc+=vd; dn-=1
    return lo+(poc+0.5)*step, lo+min(rows,up)*step, lo+max(0,dn+1)*step

def resample(t,o,h,l,c,v,period):
    # group into HTF buckets of 'period' seconds
    buckets={}
    for i in range(len(t)):
        b=t[i]//period
        if b not in buckets: buckets[b]=[t[i],o[i],h[i],l[i],c[i],v[i]]
        else:
            x=buckets[b]; x[2]=max(x[2],h[i]); x[3]=min(x[3],l[i]); x[4]=c[i]; x[5]+=v[i]
    keys=sorted(buckets); return keys,[buckets[k] for k in keys]

def pivots(series, length, right=1):
    n=len(series); ph=[None]*n; pl=[None]*n
    for i in range(length, n-right):
        seg=series[i-length:i+right+1]
        if series[i]==max(seg) and seg.count(series[i])==1: ph[i+right]=i
        if series[i]==min(seg) and seg.count(series[i])==1: pl[i+right]=i
    return ph,pl

def run(path, htf_period=86400, va_days=20, profRows=50, vaPct=0.70,
        pivLen=5, mfLen=14, mfLook=10, edgeAtr=0.5,
        maxLossUsd=100, feeUsd=8.0, qty=1.0, trailAtr=2.5, trailStart=75.0,
        cutBeyond=True, maxBars=400, tlo_frac=0.0, thi_frac=1.0, label=""):
    t,o,h,l,c,v=load(path)
    n=len(c)
    A=atr(h,l,c,14)
    hlc3=[(h[i]+l[i]+c[i])/3 for i in range(n)]
    esa=ema(hlc3,9); d=ema([abs(hlc3[i]-esa[i]) for i in range(n)],9)
    ci=[(hlc3[i]-esa[i])/(0.015*d[i]) if d[i] else 0 for i in range(n)]
    wt1=ema(ci,12)
    MF=mfi(h,l,c,v,mfLen)
    # HTF value area (previous completed HTF bar's rolling profile)
    hk,hb=resample(t,o,h,l,c,v,htf_period)
    htfVAH={}; htfVAL={}
    for idx in range(len(hb)):
        lo_i=max(0,idx-va_days+1)
        hs=[hb[j][2] for j in range(lo_i,idx+1)]; ls=[hb[j][3] for j in range(lo_i,idx+1)]; vs=[hb[j][5] for j in range(lo_i,idx+1)]
        p=profile(hs,ls,vs,profRows,vaPct)
        if p: _,vah,val=p; htfVAH[hk[idx]]=vah; htfVAL[hk[idx]]=val
    def htf_va(ti):
        b=ti//htf_period - 1  # previous completed HTF bucket
        return htfVAH.get(b), htfVAL.get(b)
    # price & WT pivots for divergence + SFP swings
    pph,ppl=pivots(c,pivLen)       # price pivots (on close) for divergence pairing
    sph,spl=pivots(h,pivLen)       # swing highs for SFP (use highs/lows)
    _,spl2=pivots(l,pivLen)
    # track last two confirmed price pivot lows/highs with WT values
    lastPL=[]; lastPH=[]
    swHi=None; swLo=None
    pos=0; entry=0; stop=0; ebar=0; mae=0; maxfav=0; trailon=False
    nTot=0; nWin=0; gWin=0; gLoss=0; net=0; best=0; worst=0; peak=0; mdd=0; fees=0
    nLong=0; nShort=0; exStop=0; exCut=0; exTime=0
    for i in range(n):
        # update swings for SFP (confirmed pivots from highs/lows)
        if sph[i] is not None: swHi=h[sph[i]]
        if spl2[i] is not None: swLo=l[spl2[i]]
        # update divergence pivot memory (price close pivots)
        if ppl[i] is not None:
            pi=ppl[i]; lastPL.append((pi, c[pi], wt1[pi])); lastPL=lastPL[-2:]
        if pph[i] is not None:
            pi=pph[i]; lastPH.append((pi, c[pi], wt1[pi])); lastPH=lastPH[-2:]
        bullDiv = len(lastPL)==2 and lastPL[1][1]<lastPL[0][1] and lastPL[1][2]>lastPL[0][2] and (i-lastPL[1][0])<=pivLen+2
        bearDiv = len(lastPH)==2 and lastPH[1][1]>lastPH[0][1] and lastPH[1][2]<lastPH[0][2] and (i-lastPH[1][0])<=pivLen+2
        bullSFP = swLo is not None and l[i]<swLo and c[i]>swLo
        bearSFP = swHi is not None and h[i]>swHi and c[i]<swHi
        moneyIn = MF[i] is not None and i>=mfLook and MF[i]>MF[i-mfLook]
        moneyOut= MF[i] is not None and i>=mfLook and MF[i]<MF[i-mfLook]
        VAH,VAL = htf_va(t[i])
        # manage open  (STRICTLY CAUSAL: check exit against the stop as it stood
        # coming into the bar, BEFORE ratcheting with this bar's extreme)
        if pos!=0 and i>ebar:
            adv=entry-l[i] if pos==1 else h[i]-entry
            if adv>mae: mae=adv
            done=False; ex=None; kind=None
            if pos==1:
                if l[i]<=stop: ex=stop; done=True; kind='stop'
            else:
                if h[i]>=stop: ex=stop; done=True; kind='stop'
            if not done and cutBeyond and VAL is not None and VAH is not None and ((pos==1 and c[i]<VAL) or (pos==-1 and c[i]>VAH)):
                ex=c[i]; done=True; kind='cut'
            if not done and (i-ebar)>=maxBars: ex=c[i]; done=True; kind='time'
            if done:
                pnl=(ex-entry)*(1 if pos==1 else -1)*qty; nt=pnl-feeUsd; fees+=feeUsd; net+=nt; nTot+=1
                if nt>=0: nWin+=1; gWin+=nt
                else: gLoss+=-nt
                best=max(best,nt); worst=min(worst,nt); peak=max(peak,net); mdd=max(mdd,peak-net); pos=0
                if kind=='stop': exStop+=1
                elif kind=='cut': exCut+=1
                else: exTime+=1
                if VERBOSE:
                    import datetime as _dt
                    print(f"    {'LONG' if nt==pnl-feeUsd and True else ''} entry@{entry:.0f} exit@{ex:.0f} bars={i-ebar} pnl=${nt:.0f} [{kind}] "
                          f"{_dt.datetime.utcfromtimestamp(t[ebar]).strftime('%Y-%m-%d %H:%M')}->{_dt.datetime.utcfromtimestamp(t[i]).strftime('%m-%d %H:%M')}")
            else:
                # ratchet AFTER the exit check, for future bars only
                ext=h[i] if pos==1 else l[i]
                maxfav=max(maxfav,ext) if pos==1 else min(maxfav,ext)
                favU=(maxfav-entry if pos==1 else entry-maxfav)*qty
                if not trailon and favU>=trailStart: trailon=True
                if trailon and A[i]:
                    ts=maxfav-trailAtr*A[i] if pos==1 else maxfav+trailAtr*A[i]
                    stop=max(stop,ts) if pos==1 else min(stop,ts)
        # entry: reversal at HTF value edge + SFP + divergence + money flow
        tlo=int(tlo_frac*n); thi=int(thi_frac*n)
        if pos==0 and tlo<=i<=thi and A[i] and VAH is not None and VAL is not None:
            nearLow = l[i] <= VAL + edgeAtr*A[i]
            nearHigh= h[i] >= VAH - edgeAtr*A[i]
            longSig = nearLow and bullSFP and bullDiv and moneyIn
            shortSig= nearHigh and bearSFP and bearDiv and moneyOut and not longSig
            if longSig:
                pos=1; entry=c[i]; ebar=i; mae=0; maxfav=c[i]; trailon=False; nLong+=1
                stop=c[i]-maxLossUsd/qty          # fixed cap, correct side
            elif shortSig:
                pos=-1; entry=c[i]; ebar=i; mae=0; maxfav=c[i]; trailon=False; nShort+=1
                stop=c[i]+maxLossUsd/qty           # fixed cap, correct side
    wr=nWin/nTot*100 if nTot else 0
    aw=gWin/nWin if nWin else 0; al=gLoss/(nTot-nWin) if (nTot-nWin) else 0
    payoff=aw/al if al else 0; exp=net/nTot if nTot else 0
    import datetime
    span=f"{datetime.datetime.utcfromtimestamp(t[0]).date()}->{datetime.datetime.utcfromtimestamp(t[-1]).date()}"
    print(f"[{label}] {span} trades={nTot}(L{nLong}/S{nShort}) win%={wr:.1f} payoff={payoff:.2f}x avgW=${aw:.0f} avgL=${al:.0f} NET=${net:.0f} exp=${exp:.1f} best=${best:.0f} worst=${worst:.0f} maxDD=${mdd:.0f} exits[stop{exStop}/cut{exCut}/time{exTime}]")

if __name__=="__main__":
    print("REVERSAL CONFLUENCE: HTF value-area edge + SFP + divergence + money-flow")
    print("--- 1h chart, DAILY value area ---")
    run("/tmp/btc_1h.csv", htf_period=86400, va_days=20, label="1h/dailyVA")
    print("--- 6h chart, DAILY value area ---")
    run("/tmp/btc_6h.csv", htf_period=86400, va_days=20, label="6h/dailyVA")
    print("--- OUT-OF-SAMPLE SPLIT (6h, 2yr) ---")
    run("/tmp/btc_6h.csv", htf_period=86400, va_days=20, tlo_frac=0.0, thi_frac=0.5, label="6h FIRST half")
    run("/tmp/btc_6h.csv", htf_period=86400, va_days=20, tlo_frac=0.5, thi_frac=1.0, label="6h SECOND half")
    print("--- OUT-OF-SAMPLE SPLIT (1h, 1yr) ---")
    run("/tmp/btc_1h.csv", htf_period=86400, va_days=20, tlo_frac=0.0, thi_frac=0.5, label="1h FIRST half")
    run("/tmp/btc_1h.csv", htf_period=86400, va_days=20, tlo_frac=0.5, thi_frac=1.0, label="1h SECOND half")
