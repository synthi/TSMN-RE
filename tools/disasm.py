#!/usr/bin/env python3
"""Desensamble Thumb Cortex-M4 con capstone para TSNM"""
from capstone import Cs, CS_ARCH_ARM, CS_MODE_THUMB
import pathlib
binp = pathlib.Path("/Users/josuearias/REPOS/TSNM-RE/docs/raw/firmware.bin")
data = binp.read_bytes()
md = Cs(CS_ARCH_ARM, CS_MODE_THUMB)
md.detail=False
def dis(addr, nbytes, label):
    print(f"\n===== {label} @ 0x{addr:08X} ({nbytes}B) =====")
    code=data[addr:addr+nbytes]
    for ins in md.disasm(code, addr):
        print(f" 0x{ins.address:08X}: {ins.mnemonic:10s} {ins.op_str:30s} ; bytes={ins.bytes.hex()}")
        if ins.mnemonic in ("bkpt",):
            break
# Entry points desde vector table
# Reset 0x1BC, NMI 0x800C, HardFault 0x800C, MemManage 0x800C?,Svc 0x87B8, PendSV 0x8A08, PIT? 0x6224, etc.
for a,lbl in [(0x1BC,"Reset_Handler"),(0x800C,"NMI/HardFault/Default?"),(0x87B8,"SVC?"),(0x8A08,"PendSV/SysTick?"),(0x6224,"IRQ40?"),(0x67D4,"IRQ41?"),(0x8B4C,"IRQ61?"),(0x8C78,"IRQ63?")]:
    dis(a & ~1, 160, lbl)
# Buscar accesos a periféricos K20: LDR literal a 0x400xxxxx
import struct
print("\n===== Referencias a perifericos 0x400xxxxx (primeras 60) =====")
# scan pool literals: palabras 0x400xxxxx en bin
for off in range(0,len(data)-4,4):
    v=struct.unpack_from("<I",data,off)[0]
    if 0x40000000 <= v <= 0x400FFFFF:
        # contexto: buscar LDR cercano? solo listar
        if off<0xC000:
            print(f" pool @file 0x{off:05X} (flash 0x{off:08X}) -> 0x{v:08X}")
            if off>0xB000: break
print("\nPerifericos K20 base conocidos:")
print(" SIM 0x40047000 PORTA-E 0x40049000-4004D000 GPIO 0x400FF000 I2C0 0x40066000 I2C1 0x40067000 SPI0 0x4002C000 SPI1 0x4002D000 ADC0 0x4003B000 ADC1 0x400BB000 DAC0 0x400CC000 FTM0-2 PIT 0x40037000 USB0 0x40072000 TSI 0x40045000 UART0-3 RTC WDOG MCG OSC")
