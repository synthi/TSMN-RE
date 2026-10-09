#!/usr/bin/env python3
"""HEX -> BIN + mapa memoria MK20DX256 para TSNM v30"""
import pathlib, struct, sys
hexpath = pathlib.Path("/Users/josuearias/REPOS/TSNM-RE/TSNM_4U_v30.hex")
outbin = pathlib.Path("/Users/josuearias/REPOS/TSNM-RE/docs/raw/firmware.bin")
lines = hexpath.read_text().splitlines()
upper = 0
segs = []
for l in lines:
    l=l.strip()
    if not l: continue
    n=int(l[1:3],16); addr=int(l[3:7],16); typ=int(l[7:9],16)
    data=l[9:9+n*2]
    if typ==0:
        absaddr=(upper<<16)+addr
        segs.append((absaddr, bytes.fromhex(data) if data else b''))
    elif typ==4:
        upper=int(data,16)
    elif typ==1:
        break
print(f"lineas: {len(lines)} segmentos: {len(segs)}")
start=min(a for a,_ in segs); end=max(a+len(d) for a,d in segs)
total=sum(len(d) for _,d in segs)
print(f"rango {start:08X}..{end-1:08X} total {total} ({total/1024:.1f}KB) flash 256KB={256*1024} libre~{256*1024-total}")
# gaps
cur=start
gaps=[]
for a,d in sorted(segs):
    if a>cur:
        gaps.append((cur,a,a-cur))
    cur=max(cur,a+len(d))
print(f"gaps: {len(gaps)}")
for g in gaps[:30]:
    print(f" gap {g[0]:08X}-{g[1]-1:08X} sz {g[2]}")
# build flat bin from 0x0 to end
size=end-start
flat=bytearray(b'\xFF'*size)
for a,d in segs:
    flat[a-start:a-start+len(d)]=d
outbin.write_bytes(flat)
print(f"bin -> {outbin} {len(flat)} bytes")
# vector table (first 256 bytes = 64 vectores)
print("\n== Vector Table (LE32) ==")
for i in range(0,64):
    v=struct.unpack_from("<I",flat, i*4)[0]
    if i<16 or v not in (0x00007FC5,0x0000800D):
        print(f" [{i:3d}] off 0x{i*4:03X} = 0x{v:08X}{' (THUMB? +1)' if v&1 else ''}")
# busqueda strings ASCII
import re
data=bytes(flat)
strs=[m.group().decode() for m in re.finditer(b'[ -~]{5,}', data)]
print(f"\n== strings >=5 ({len(strs)}) primeras 100 ==")
for s in strs[:100]:
    print(repr(s))
# entropia / FF / 00 stats
ff=data.count(0xFF); zz=data.count(0x00)
print(f"\nFF={ff} ({ff/len(data)*100:.1f}%) 00={zz} ({zz/len(data)*100:.1f}%)")
# Buscar tabla final de punteros 1FFFxxxx
ptrs=[struct.unpack_from("<I",data,o)[0] for o in range(len(data)-4) if 0x1FFF8000<=struct.unpack_from("<I",data,o)[0]<=0x20008000]
print(f"punteros RAM-low/high hallados: {len(ptrs)} ej: {[hex(x) for x in ptrs[:20]]}")
