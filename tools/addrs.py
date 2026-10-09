#!/usr/bin/env python3
import pathlib
for name in ["TSNM_4U_v30.hex","TSNM_mkII_v50_4U_t32.hex"]:
    p=f"/Users/josuearias/REPOS/TSNM-RE/tsnm m2 reference/{name}"
    print("====",name)
    for l in pathlib.Path(p).read_text().splitlines():
        if l[7:9] in ("02","04","01","05","03"):
            print(l.strip())
