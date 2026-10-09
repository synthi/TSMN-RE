#!/usr/bin/env python3
import pathlib, struct, collections
def load_bin(p): return pathlib.Path(p).read_bytes()
v30 = load_bin("/Users/josuearias/REPOS/TSNM-RE/docs/raw/firmware.bin")
v50 = load_bin("/Users/josuearias/REPOS/TSNM-RE/docs/raw/mkii_v50.bin")
print("v30 len", len(v30), "v50 len", len(v50))
print("VECTORES:")
for i in [0,1,2,3,11,12,13,14,15,40,41,61,63]:
    a=struct.unpack_from("<I",v30,i*4)[0] if i*4+4<=len(v30) else 0
    b=struct.unpack_from("<I",v50,i*4)[0]
    print(f" [{i}] v30=0x{a:08X} v50=0x{b:08X} {'IGUAL' if a==b else ''}")
def pools(d):
    c=collections.Counter()
    for off in range(0,len(d)-4,4):
        v=struct.unpack_from("<I",d,off)[0]
        if 0x40000000<=v<=0x400FFFFF:
            c[v&0xFFFFF000]+=1
    return c
print("POOLS v30:", pools(v30).most_common(12))
print("POOLS v50:", pools(v50).most_common(12))
