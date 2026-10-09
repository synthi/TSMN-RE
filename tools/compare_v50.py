#!/usr/bin/env python3
"""Compara v30 vs mkII v50: tamaños, vectores, periféricos"""
import pathlib, struct
def parse(hexpath):
    upper=0; segs=[]
    for l in pathlib.Path(hexpath).read_text().splitlines():
        l=l.strip()
        if not l: continue
        n=int(l[1:3],16); addr=int(l[3:7],16); typ=int(l[7:9],16); data=l[9:9+n*2]
        if typ==0:
            segs.append((((upper<<16)+addr), bytes.fromhex(data) if data else b''))
        elif typ==4:
            upper=int(data,16)
        elif typ==1: break
    start=min(a for a,_ in segs); end=max(a+len(d) for a,d in segs)
    flat=bytearray(b'\xFF'*(end-start))
    for a,d in segs: flat[a-start:a-start+len(d)]=d
    return start,end,bytes(flat)
for name, p in [("v30-original","/Users/josuearias/REPOS/TSNM-RE/docs/raw/firmware.bin"),
                ("mkII-v50","/Users/josuearias/REPOS/TSNM-RE/tsnm m2 reference/TSNM_mkII_v50_4U_t32.hex")]:
    if name=="v30-original":
        d=pathlib.Path(p).read_bytes(); s=0; e=len(d)
    else:
        s,e,d=parse(p)
        pathlib.Path("/Users/josuearias/REPOS/TSNM-RE/docs/raw/mkii_v50.bin").write_bytes(d)
    print(f"\n===== {name} =====")
    print(f" rango {s:08X}..{e-1:08X} total {len(d)} ({len(d)/1024:.1f}KB)")
    print(" vectores:")
    for i in [0,1,2,3,11,12,13,14,15,40,41,61,63]:
        v=struct.unpack_from("<I",d,i*4)[0]
        print(f"  [{i:3d}] = 0x{v:08X}")
    # pools perifericos
    import collections
    pools=collections.Counter()
    for off in range(0,len(d)-4,4):
        v=struct.unpack_from("<I",d,off)[0]
        if 0x40000000<=v<=0x400FFFFF:
            pools[v&0xFFFFF000]+=1
    print(" bases 0x400xxxxx más usadas:")
    for k,c in pools.most_common(15):
        print(f"  0x{0x40000000+k:08X} x{c}")
