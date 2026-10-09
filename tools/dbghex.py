#!/usr/bin/env python3
import pathlib
p="/Users/josuearias/REPOS/TSNM-RE/tsnm m2 reference/TSNM_mkII_v50_4U_t32.hex"
recs=[]
for l in pathlib.Path(p).read_text().splitlines():
    l=l.strip()
    if not l: continue
    n=int(l[1:3],16); a=int(l[3:7],16); t=int(l[7:9],16)
    recs.append((t,a,n,l))
from collections import Counter
print(Counter(t for t,_,_,_ in recs))
# ver si hay solapes: mapa addr->count
m={}
up=0
for l in pathlib.Path(p).read_text().splitlines():
    l=l.strip(); n=int(l[1:3],16); a=int(l[3:7],16); t=int(l[7:9],16)
    if t==0:
        ab=(up<<16)+a
        for i in range(n):
            m[ab+i]=m.get(ab+i,0)+1
    elif t==4: up=int(l[9:13],16)
print("min",hex(min(m)),"max",hex(max(m)),"uniq",len(m),"sum",sum(1 for _ in recs if _[0]==0))
import collections
over={k:v for k,v in m.items() if v>1}
print("solapes:",len(over), list(over.items())[:10])
# dump primeras 64 palabras con última escritura
mem={}
up=0
for l in pathlib.Path(p).read_text().splitlines():
    l=l.strip(); n=int(l[1:3],16); a=int(l[3:7],16); t=int(l[7:9],16); d=l[9:9+n*2]
    if t==0:
        ab=(up<<16)+a; b=bytes.fromhex(d) if d else b''
        for i,bb in enumerate(b): mem[ab+i]=bb
    elif t==4: up=int(l[9:13],16)
import struct
for i in range(16):
    v=struct.unpack_from("<I",bytes(mem[k] for k in range(i*4,i*4+4)))[0]
    print(i, hex(v))
