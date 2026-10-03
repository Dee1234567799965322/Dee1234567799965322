import csv, sys, statistics

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
        e = x if e is None else x*k+e*(1-k)
        out[i]=e
    return out

def sma(src,n):
    out=[None]*len(src); s=0; from_i=0
    import collections
    dq=collections.deque()
    for i,x in enumerate(src):
        if x is None: x=0
        dq.append(x); s+=x
        if len(dq)>n: s-=dq.popleft()
        out[i]= s/len(dq)
    return out

def atr(h,l,c,n=14):
    tr=[0.0]*len(c)
    for i in range(len(c)):
        if i==0: tr[i]=h[i]-l[i]
        else: tr[i]=max(h[i]-l[i], abs(h[i]-c[i-1]), abs(l[i]-c[i-1]))
    return ema(tr,n)  # approx (Pine ta.atr uses RMA; EMA close enough)

def profile(h,l,v,i,look,rows,pct):
    lo_i=max(0,i-look+1)
    hs=h[lo_i:i+1]; ls=l[lo_i:i+1]; vs=v[lo_i:i+1]
    if not hs: return None
    hi=max(hs); lo=min(ls); rng=hi-lo
    if rng<=0: return None
    step=rng/rows
    bins=[0.0]*rows
    for j in range(len(hs)):
        bv=vs[j]
        if bv<=0: continue
        a=int((ls[j]-lo)/step); b=int((hs[j]-lo)/step)
        a=max(0,min(rows-1,a)); b=max(0,min(rows-1,b))
        sl=bv/(b-a+1)
        for k in range(a,b+1): bins[k]+=sl
    tot=sum(bins)
    if tot<=0: return None
    poc=bins.index(max(bins)); target=tot*pct; acc=bins[poc]
    up=poc+1; dn=poc-1
    while acc<target and (up<=rows-1 or dn>=0):
        vu=bins[up] if up<=rows-1 else -1; vd=bins[dn] if dn>=0 else -1
        if vu<0 and vd<0: break
        if vu>=vd: acc+=vu; up+=1
        else: acc+=vd; dn-=1
    POC=lo+(poc+0.5)*step; VAH=lo+min(rows,up)*step; VAL=lo+max(0,dn+1)*step
    return POC,VAH,VAL

def pivots(h,l,length):
    n=len(h); ph=[None]*n; pl=[None]*n
    for i in range(length, n-1):  # right=1
        seg_h=h[i-length:i+2]; seg_l=l[i-length:i+2]
        if h[i]==max(seg_h) and seg_h.count(h[i])==1: ph[i+1]=h[i]  # confirmed next bar
        if l[i]==min(seg_l) and seg_l.count(l[i])==1: pl[i+1]=l[i]
    return ph,pl

def run(path, useTrend=True, useSweep=True, requireWT=True,
        profLook=200, profRows=50, vaPct=0.70, trendLen=200,
        sweepLen=5, sweepWindow=3, maxLossUsd=100, feeUsd=8.0, qty=1.0,
        trailAtr=2.5, trailStart=75.0, cutOnBreak=True, maxBars=300, label=""):
    t,o,h,l,c,v=load(path)
    n=len(c)
    A=atr(h,l,c,14)
    hlc3=[(h[i]+l[i]+c[i])/3 for i in range(n)]
    esa=ema(hlc3,9); d=ema([abs(hlc3[i]-esa[i]) for i in range(n)],9)
    ci=[(hlc3[i]-esa[i])/(0.015*d[i]) if d[i] else 0 for i in range(n)]
    wt1=ema(ci,12); wt2=sma(wt1,3)
    tema=ema(c,trendLen)
    ph,pl=pivots(h,l,sweepLen)
    # precompute profile
    VAH=[None]*n; VAL=[None]*n
    for i in range(n):
        if i>=30:
            p=profile(h,l,v,i,profLook,profRows,vaPct)
            if p: _,VAH[i],VAL[i]=p
    # sweep tracking
    swHi=None; swLo=None; agoBull=10**9; agoBear=10**9
    pos=0; entry=0; stop=0; tgt=None; ebar=0; mae=0; maxfav=0; trailon=False
    nTot=0; nWin=0; gWin=0; gLoss=0; net=0; best=0; worst=0; peak=0; mdd=0; fees=0
    for i in range(n):
        if ph[i] is not None: swHi=ph[i]
        if pl[i] is not None: swLo=pl[i]
        bullSweep = swLo is not None and l[i]<swLo and c[i]>swLo
        bearSweep = swHi is not None and h[i]>swHi and c[i]<swHi
        agoBull = 0 if bullSweep else agoBull+1
        agoBear = 0 if bearSweep else agoBear+1
        # manage
        if pos!=0:
            adv = entry-l[i] if pos==1 else h[i]-entry
            if adv>mae: mae=adv
            ext = h[i] if pos==1 else l[i]
            maxfav = ext if maxfav is None else (max(maxfav,ext) if pos==1 else min(maxfav,ext))
            favU = (maxfav-entry if pos==1 else entry-maxfav)*qty
            if not trailon and favU>=trailStart: trailon=True
            if trailon and A[i]:
                ts = maxfav-trailAtr*A[i] if pos==1 else maxfav+trailAtr*A[i]
                stop = max(stop,ts) if pos==1 else min(stop,ts)
            done=False; exitpx=None
            if pos==1:
                if l[i]<=stop: exitpx=stop; done=True
                elif tgt is not None and h[i]>=tgt: exitpx=tgt; done=True
            else:
                if h[i]>=stop: exitpx=stop; done=True
                elif tgt is not None and l[i]<=tgt: exitpx=tgt; done=True
            if not done and cutOnBreak and VAL[i] is not None and VAH[i] is not None and ((pos==1 and c[i]<VAL[i]) or (pos==-1 and c[i]>VAH[i])):
                exitpx=c[i]; done=True
            if not done and (i-ebar)>=maxBars:
                exitpx=c[i]; done=True
            if done:
                pnl=(exitpx-entry)*(1 if pos==1 else -1)*qty
                nt=pnl-feeUsd; fees+=feeUsd; net+=nt; nTot+=1
                if nt>=0: nWin+=1; gWin+=nt
                else: gLoss+=-nt
                best=max(best,nt); worst=min(worst,nt)
                peak=max(peak,net); mdd=max(mdd,peak-net)
                pos=0
        # entry
        if pos==0 and A[i] and VAL[i] is not None and VAH[i] is not None:
            trendUp=c[i]>tema[i] if tema[i] else False
            trendDn=c[i]<tema[i] if tema[i] else False
            wtU=wt1[i]>=wt2[i]; wtD=wt1[i]<=wt2[i]
            bOk = (not useSweep) or agoBull<=sweepWindow
            sOk = (not useSweep) or agoBear<=sweepWindow
            longSig = l[i]<VAL[i] and c[i]>VAL[i] and ((not requireWT) or wtU) and bOk and ((not useTrend) or trendUp)
            shortSig= h[i]>VAH[i] and c[i]<VAH[i] and ((not requireWT) or wtD) and sOk and ((not useTrend) or trendDn) and not longSig
            if longSig:
                pos=1; entry=c[i]; ebar=i; mae=0; maxfav=c[i]; trailon=False
                sp=VAL[i]-0.5*A[i]
                if maxLossUsd>0: sp=max(sp, c[i]-maxLossUsd/qty)
                stop=sp; tgt=None
            elif shortSig:
                pos=-1; entry=c[i]; ebar=i; mae=0; maxfav=c[i]; trailon=False
                sp=VAH[i]+0.5*A[i]
                if maxLossUsd>0: sp=min(sp, c[i]+maxLossUsd/qty)
                stop=sp; tgt=None
    wr = nWin/nTot*100 if nTot else 0
    aw = gWin/nWin if nWin else 0
    al = gLoss/(nTot-nWin) if (nTot-nWin) else 0
    payoff = aw/al if al else 0
    exp = net/nTot if nTot else 0
    import datetime
    span=f"{datetime.datetime.utcfromtimestamp(t[0]).date()}→{datetime.datetime.utcfromtimestamp(t[-1]).date()}"
    print(f"[{label}] {span}  trades={nTot} win%={wr:.1f} payoff={payoff:.2f}x "
          f"avgW=${aw:.0f} avgL=${al:.0f} NET=${net:.0f} exp=${exp:.1f} "
          f"best=${best:.0f} worst=${worst:.0f} maxDD=${mdd:.0f}")
    return dict(trades=nTot,win=wr,payoff=payoff,net=net,mdd=mdd,best=best,worst=worst,exp=exp)

if __name__=="__main__":
    path=sys.argv[1] if len(sys.argv)>1 else "/tmp/btc_1h.csv"
    print("=== FULL STRATEGY (trend filter ON) ===")
    run(path, useTrend=True, label="trend ON")
    print("=== trend filter OFF (for comparison) ===")
    run(path, useTrend=False, label="trend OFF")
    print("=== longs only / shorts only (trend ON) ===")
    # quick direction split via monkey: rerun with useShort disabled not param; skip
