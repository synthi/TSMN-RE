#!/usr/bin/env python3
import pathlib, struct, collections, re
lo=pathlib.Path("/Users/josuearias/REPOS/TSNM-RE/docs/raw/mkii_lo.bin").read_bytes()
hi=pathlib.Path("/Users/josuearias/REPOS/TSNM-RE/docs/raw/mkii_hi.bin").read_bytes()
print(f"lo {len(lo)} hi {len(hi)} total {len(lo)+len(hi)} flash 256K libre {256*1024-len(lo)-len(hi)}")
for i in [0,1,2,3,14,15,40,41,61,63]:
    v=struct.unpack_from("<I",lo,i*4)[0]
    print(f" V[{i}] = 0x{v:08X}")
def pools(d, base=0):
    c=collections.Counter()
    for off in range(0,len(d)-4,4):
        v=struct.unpack_from("<I",d,off)[0]
        if 0x40000000<=v<=0x400FFFFF: c[v&0xFFFFF000]+=1
    return c
print("POOLS lo:",[(hex(k),v) for k,v in pools(lo).most_common(16)])
print("POOLS hi:",[(hex(k),v) for k,v in pools(hi).most_common(16)])
for label,d,base in [("lo",lo,0x0),("hi",hi,0x10000)]:
    ss=[m.group().decode() for m in re.finditer(b'[ -~]{5,}', d)]
    print(f"{label} strings={len(ss)}")
    interesting=[x for x in ss if len(x.strip())>8 or "TSNM" in x or "INPUT" in x]
    for x in interesting[:50]: print(" ",repr(x))
