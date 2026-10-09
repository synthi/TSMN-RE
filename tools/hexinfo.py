#!/usr/bin/env python3
import pathlib
def info(h):
    up=0; n0=0; ext=[]; last=None; total=0; mn=None; mx=0
    for l in pathlib.Path(h).read_text().splitlines():
        l=l.strip()
        if not l: continue
        n=int(l[1:3],16); a=int(l[3:7],16); t=int(l[7:9],16); d=l[9:9+n*2]
        if t==0:
            ab=(up<<16)+a; total+=n
            if mn is None or ab<mn: mn=ab
            if ab+n>mx: mx=ab+n
            n0+=1; last=(ab,n)
        elif t==4: up=int(d,16); ext.append((up,d))
        elif t==1: pass
    return {"segs":n0,"ext":ext,"total":total,"min":mn,"max":mx,"last":last}
for p in ["/Users/josuearias/REPOS/TSNM-RE/tsnm m2 reference/TSNM_4U_v30.hex","/Users/josuearias/REPOS/TSNM-RE/tsnm m2 reference/TSNM_mkII_v50_4U_t32.hex"]:
    print(p, info(p))
