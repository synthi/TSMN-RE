#!/usr/bin/env python3
import pathlib, struct, collections
def parse_hex(h):
    up=0; segs=[]
    for l in pathlib.Path(h).read_text().splitlines():
        l=l.strip()
        if not l: continue
        n=int(l[1:3],16); a=int(l[3:7],16); t=int(l[7:9],16); d=l[9:9+n*2]
        if t==0: segs.append((((up<<16)+a), bytes.fromhex(d) if d else b''))
        elif t==4: up=int(d,16)
        elif t==1: break
    s=min(a for a,_ in segs); e=max(a+len(d) for a,d in segs)
    f=bytearray(b'\xFF'*(e-s))
    for a,d in segs: f[a-s:a-s+len(d)]=d
    return s,e,bytes(f)
s30,e30,d30=parse_hex("/Users/josuearias/REPOS/TSNM-RE/tsnm m2 reference/TSNM_4U_v30.hex")
s50,e50,d50=parse_hex("/Users/josuearias/REPOS/TSNM-RE/tsnm m2 reference/TSNM_mkII_v50_4U_t32.hex")
pathlib.Path("/Users/josuearias/REPOS/TSNM-RE/docs/raw/mkii_v50_flat.bin").write_bytes(d50)
pathlib.Path("/Users/josuearias/REPOS/TSNM-RE/docs/raw/v30_flat.bin").write_bytes(d30)
print(f"v30 rango {s30:08X}..{e30-1:08X} len {len(d30)}")
print(f"v50 rango {s50:08X}..{e50-1:08X} len {len(d50)}")
for i in [0,1,2,3,11,12,13,14,15,40,41,61,63]:
    a=struct.unpack_from("<I",d30,i*4)[0]; b=struct.unpack_from("<I",d50,i*4)[0]
    print(f" [{i}] v30=0x{a:08X} v50=0x{b:08X} {'IGUAL' if a==b else ''}")
def pools(d):
    c=collections.Counter()
    for off in range(0,len(d)-4,4):
        v=struct.unpack_from("<I",d,off)[0]
        if 0x40000000<=v<=0x400FFFFF: c[v&0xFFFFF000]+=1
    return c
print("POOLS v30:", [(hex(k),v) for k,v in pools(d30).most_common(14)])
print("POOLS v50:", [(hex(k),v) for k,v in pools(d50).most_common(14)])
# strings ASCII >=6 en v50
import re
ss=[m.group().decode() for m in re.finditer(b'[ -~]{6,}', d50)]
print(f"v50 strings={len(ss)}")
for x in ss[:60]: print(repr(x))
