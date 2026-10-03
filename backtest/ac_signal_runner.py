import csv, sys
import backtest2 as B  # ema, sma, atr, profile, resample, pivots

def load(path):
    o=[];h=[];l=[];c=[];v=[];t=[]
    with open(path) as f:
        r=csv.reader(f); next(r)
        for row in r:
            t.append(int(row[0])); l.append(float(row[1])); h.append(float(row[2]))
            o.append(float(row[3])); c.append(float(row[4])); v.append(float(row[5]))
    return t,o,h,l,c,v

def rolling_vwap(h,l,c,v,win):
    tp=[(h[i]+l[i]+c[i])/3 for i in range(len(c))]
    import collections
    dqpv=collections.deque(); dqv=collections.deque(); spv=0; sv=0
    vwap=[None]*len(c); sd=[None]*len(c)
    dqtp=collections.deque()
    for i in range(len(c)):
        dqpv.append(tp[i]*v[i]); spv+=tp[i]*v[i]; dqv.append(v[i]); sv+=v[i]; dqtp.append(tp[i])
        if len(dqpv)>win:
            spv-=dqpv.popleft(); sv-=dqv.popleft(); dqtp.popleft()
        vwap[i]=spv/sv if sv>0 else tp[i]
        m=sum(dqtp)/len(dqtp); sd[i]=(sum((x-m)**2 for x in dqtp)/len(dqtp))**0.5
    return vwap,sd

def run(path, label="", osLevel=53.0, locTol=0.0012, csigWindow=3, cooldown=85,
        maxLossUsd=100.0, qty=1.0, feeUsd=8.0, slipUsd=2.0, trailAtr=2.5,
        trailStart=75.0, cutBeyond=True, maxBars=300, vwapWin=48,
        htf_period=86400, va_days=20, extreme=True, resample_to=None):
    t,o,h,l,c,v=load(path)
    if resample_to:
        # resample base bars to resample_to seconds (e.g. 90m from 30m)
        keys,bars=B.resample(t,o,h,l,c,v,resample_to)
        t=[b[0] for b in bars]; o=[b[1] for b in bars]; h=[b[2] for b in bars]
        l=[b[3] for b in bars]; c=[b[4] for b in bars]; v=[b[5] for b in bars]
    n=len(c)
    A=B.atr(h,l,c,14)
    hlc3=[(h[i]+l[i]+c[i])/3 for i in range(n)]
    esa=B.ema(hlc3,9); d=B.ema([abs(hlc3[i]-esa[i]) for i in range(n)],9)
    ci=[(hlc3[i]-esa[i])/(0.015*d[i]) if d[i] else 0 for i in range(n)]
    wt1=B.ema(ci,12); wt2=B.sma(wt1,3)
    vwap,sd=rolling_vwap(h,l,c,v,vwapWin)
    # HTF daily value area (previous completed bucket)
    hk,hb=B.resample(t,o,h,l,c,v,htf_period)
    VAH={}; VAL={}; POC={}
    for idx in range(len(hb)):
        lo_i=max(0,idx-va_days+1)
        hs=[hb[j][2] for j in range(lo_i,idx+1)]; ls=[hb[j][3] for j in range(lo_i,idx+1)]; vs=[hb[j][5] for j in range(lo_i,idx+1)]
        p=B.profile(hs,ls,vs,50,0.70)
        if p: POC[hk[idx]],VAH[hk[idx]],VAL[hk[idx]]=p
    def va(ti):
        b=ti//htf_period-1
        return VAH.get(b),VAL.get(b),POC.get(b)
    # triggers
    def crossUp(i): return i>0 and wt1[i-1]<=wt2[i-1] and wt1[i]>wt2[i]
    def crossDn(i): return i>0 and wt1[i-1]>=wt2[i-1] and wt1[i]<wt2[i]
    buyTrig=[False]*n; sellTrig=[False]*n
    for i in range(n):
        buyTrig[i]= crossUp(i) and (not extreme or wt1[i]<=-osLevel)
        sellTrig[i]= crossDn(i) and (not extreme or wt1[i]>=osLevel)
    def near(px,lv): return lv is not None and abs(px-lv)/px<=locTol
    pos=0; entry=0; stop=0; ebar=0; mae=0; maxfav=0; trailon=False; lastSig=-10**9
    pend=0  # pending dir for next-bar-open entry
    nTot=0;nWin=0;gWin=0;gLoss=0;net=0;best=0;worst=0;peak=0;mdd=0;fees=0;nLong=0;nShort=0
    exStop=0;exCut=0;exOpp=0;exTime=0
    for i in range(n):
        vah,val,poc=va(t[i])
        # --- execute pending entry at THIS bar's open (next-bar-open fill) ---
        if pend!=0 and pos==0:
            pos=pend; entry=o[i]+ (slipUsd if pend==1 else -slipUsd)/qty
            ebar=i; mae=0; maxfav=o[i]; trailon=False
            stop= entry-maxLossUsd/qty if pend==1 else entry+maxLossUsd/qty
            if pend==1: nLong+=1
            else: nShort+=1
            pend=0
        # --- manage open (causal) ---
        if pos!=0 and i>=ebar:
            adv=entry-l[i] if pos==1 else h[i]-entry
            if adv>mae: mae=adv
            done=False; ex=None; kind=None
            if pos==1 and l[i]<=stop: ex=stop; done=True; kind='stop'
            elif pos==-1 and h[i]>=stop: ex=stop; done=True; kind='stop'
            if not done and cutBeyond and val is not None and vah is not None and ((pos==1 and c[i]<val) or (pos==-1 and c[i]>vah)):
                ex=c[i]; done=True; kind='cut'
            if not done and (i-ebar)>=maxBars: ex=c[i]; done=True; kind='time'
            if done:
                exx=ex - (slipUsd if pos==1 else -slipUsd)/qty
                pnl=(exx-entry)*(1 if pos==1 else -1)*qty; nt=pnl-feeUsd; fees+=feeUsd; net+=nt; nTot+=1
                if nt>=0: nWin+=1; gWin+=nt
                else: gLoss+=-nt
                best=max(best,nt); worst=min(worst,nt); peak=max(peak,net); mdd=max(mdd,peak-net); pos=0
                if kind=='stop':exStop+=1
                elif kind=='cut':exCut+=1
                else:exTime+=1
            else:
                ext=h[i] if pos==1 else l[i]
                maxfav=max(maxfav,ext) if pos==1 else min(maxfav,ext)
                favU=(maxfav-entry if pos==1 else entry-maxfav)*qty
                if not trailon and favU>=trailStart: trailon=True
                if trailon and A[i]:
                    ts=maxfav-trailAtr*A[i] if pos==1 else maxfav+trailAtr*A[i]
                    stop=max(stop,ts) if pos==1 else min(stop,ts)
        # --- signal at bar i (close), fire pending for next bar ---
        if vah is not None and A[i]:
            # location now
            buyLoc = near(l[i],val) or near(l[i],vwap[i]-sd[i]) or near(l[i],vwap[i]-2*sd[i]) or near(l[i],poc)
            sellLoc= near(h[i],vah) or near(h[i],vwap[i]+sd[i]) or near(h[i],vwap[i]+2*sd[i]) or near(h[i],poc)
            # trigger within window
            bT=any(buyTrig[max(0,i-csigWindow+1):i+1]); sT=any(sellTrig[max(0,i-csigWindow+1):i+1])
            buySig = bT and buyLoc
            sellSig= sT and sellLoc and not buySig
            if (buySig or sellSig) and (i-lastSig)>=cooldown:
                sigdir=1 if buySig else -1
                if pos==0 and pend==0:
                    pend=sigdir; lastSig=i
                elif pos!=0 and sigdir==-pos:
                    # opposite signal closes open trade at next open; then can re-enter
                    # close now at this close (event), record
                    exx=c[i]-(slipUsd if pos==1 else -slipUsd)/qty
                    pnl=(exx-entry)*(1 if pos==1 else -1)*qty; nt=pnl-feeUsd; fees+=feeUsd; net+=nt; nTot+=1
                    if nt>=0: nWin+=1; gWin+=nt
                    else: gLoss+=-nt
                    best=max(best,nt); worst=min(worst,nt); peak=max(peak,net); mdd=max(mdd,peak-net); pos=0; exOpp+=1
                    pend=sigdir; lastSig=i
    wr=nWin/nTot*100 if nTot else 0
    aw=gWin/nWin if nWin else 0; al=gLoss/(nTot-nWin) if (nTot-nWin) else 0
    payoff=aw/al if al else 0; exp=net/nTot if nTot else 0
    import datetime
    span=f"{datetime.datetime.utcfromtimestamp(t[0]).date()}->{datetime.datetime.utcfromtimestamp(t[-1]).date()}"
    print(f"[{label}] {span} trades={nTot}(L{nLong}/S{nShort}) win%={wr:.1f} payoff={payoff:.2f}x avgW=${aw:.0f} avgL=${al:.0f} NET=${net:.0f} exp=${exp:.1f} best=${best:.0f} worst=${worst:.0f} maxDD=${mdd:.0f} exits[stop{exStop}/cut{exCut}/opp{exOpp}/time{exTime}]")

if __name__=="__main__":
    print("AC-core signal (WT cross in extreme @ value/VWAP location) + runner exit, next-bar-open fill")
    run("/tmp/btc_1h.csv", label="1h")
    run("/tmp/btc_6h.csv", label="6h")
