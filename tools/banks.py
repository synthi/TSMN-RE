#!/usr/bin/env python3
import pathlib, struct, collections, re
def banks(h):
    up=0; m={}
    for l in pathlib.Path(h).read_text().splitlines():
        l=l.strip()
        if not l: continue
        n=int(l[1:3],16); a=int(l[3:7],16); t=int(l[7:9],16); d=l[9:9+n*2]
        if t==0:
            ab=(up<<16)+a; b=bytes.fromhex(d) if d else b''
            for i,bb in enumerate(b): m[ab+i]=bb
        elif t in (2,4):
            if t==4: up=int(d,16)
            else: up=int(d,16)  # segmento: <<4
                # tipo 02: base = int(d,16)<<4
            if t==2: up=int(d,16)<<4 >>16  # lo resolvemos abajo
    # reparse correcto tipo 02
    up=0; m={}
    for l in pathlib.Path(h).read_text().splitlines():
        l=l.strip(); n=int(l[1:3],16); a=int(l[3:7],16); t=int(l[7:9],16); d=l[9:9+n*2]
        if t==0:
            ab=up+a; b=bytes.fromhex(d) if d else b''
            for i,bb in enumerate(b): m[ab+i]=bb
        elif t==4: up=int(d,16)<<16
        elif t==2: up=int(d,16)<<4
    return m
for name in ["TSNM_4U_v30.hex","TSNM_mkII_v50_4U_t32.hex"]:
    m=banks(f"/Users/josuearias/REPOS/TSNM-RE/tsnm m2 reference/{name}")
    mn=min(m); mx=max(m)
    print(f"{name}: {mn:08X}..{mx:08X} uniq {len(m)}")
    # histograma por bancos 64K
    from collections import Counter
    c=Counter(k>>16 for k in m)
    print(" ",dict(c))
m50=banks("/Users/josuearias/REPOS/TSNM-RE/tsnm m2 reference/TSNM_mkII_v50_4U_t32.hex")
# vectores banco 0x0
for i in [0,1,2,3,11,12,13,14,15]:
    v=struct.unpack("<I",bytes(m50[k] for k in range(i*4,i*4+4)))[0]
    print(f" V[{i}] = 0x{v:08X}")
# vectores banco 0x10000
print("Banco 0x10000 primeros:")
for i in range(8):
    base=0x10000+i*4
    v=struct.unpack("<I",bytes(m50[base+k] for k in range(4)))[0]
    print(f"  0x{base:08X} = 0x{v:08X}")
# strings en banco alto (codigo real?)
hi=bytes(m50[k] for k in sorted(k for k in m50 if k>=0x10000))
ss=[x.group().decode() for x in re.finditer(b'[ -~]{6,}', hi)]
print(f"strings hi={len(ss)}")
for x in ss[:80]: print(repr(x))
pathlib.Path("/Users/josuearias/REPOS/TSNM-RE/docs/raw/mkii_hi.bin").write_bytes(hi)
lo=bytes(m50[k] for k in sorted(k for k in m50 if k<0x10000))
pathlib.Path("/Users/josuearias/REPOS/TSNM-RE/docs/raw/mkii_lo.bin").write_bytes(lo)
print(f"lo {len(lo)} hi {len(hi)}")
