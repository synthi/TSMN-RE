#!/usr/bin/env python3
import pathlib, struct, collections, re
def flat(h):
    up=0; m={}
    for l in pathlib.Path(h).read_text().splitlines():
        l=l.strip()
        if not l: continue
        n=int(l[1:3],16); a=int(l[3:7],16); t=int(l[7:9],16); d=l[9:9+n*2]
        if t==0:
            ab=(up<<16)+a; b=bytes.fromhex(d) if d else b''
            for i,bb in enumerate(b): m[ab+i]=bb
        elif t==4: up=int(d,16)
    mn=min(m); mx=max(m)
    f=bytearray(b'\xFF'*(mx+1-mn))
    for k,v in m.items(): f[k-mn]=v
    return mn,mx,bytes(f)
mn30,mx30,d30=flat("/Users/josuearias/REPOS/TSNM-RE/tsnm m2 reference/TSNM_4U_v30.hex")
mn50,mx50,d50=flat("/Users/josuearias/REPOS/TSNM-RE/tsnm m2 reference/TSNM_mkII_v50_4U_t32.hex")
print(f"v30 {mn30:08X}..{mx50:08X} len {len(d30)}")
print(f"v50 {mn50:08X}..{mx50:08X} len {len(d50)}")
pathlib.Path("/Users/josuearias/REPOS/TSNM-RE/docs/raw/mkii_v50_true.bin").write_bytes(d50)
for i in [0,1,2,3,11,12,13,14,15,40,41,61,63]:
    a=struct.unpack_from("<I",d30,i*4)[0]; b=struct.unpack_from("<I",d50,i*4)[0]
    print(f" [{i}] v30=0x{a:08X} v50=0x{b:08X} {'IGUAL' if a==b else ''}")
def pools(d):
    c=collections.Counter()
    for off in range(0,len(d)-4,4):
        v=struct.unpack_from("<I",d,off)[0]
        if 0x40000000<=v<=0x400FFFFF: c[v&0xFFFFF000]+=1
    return c
print("v30",[(hex(k),v) for k,v in pools(d30).most_common(14)])
print("v50",[(hex(k),v) for k,v in pools(d50).most_common(14)])
ss=[m.group().decode() for m in re.finditer(b'[ -~]{6,}', d50)]
print(len(ss))
for x in ss:
    if "TSNM" in x or "INPUT" in x or "C C#" in x or "SEIODO" in x: print(repr(x))
print("--- primeras 40 strings ---")
for x in ss[:40]: print(repr(x))
