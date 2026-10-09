# M3 — Mapa firmware TSNM_4U_v30.hex (MK20DX256VLH7, Cortex-M4 Thumb-2)

BIN: `docs/raw/firmware.bin` 47608B (46.5KB), rango 0x00000000-0x0000B9F7, 0 gaps, libre ~209.5KB hasta 0x3FFFF. LST: `docs/raw/firmware.lst` 18985 líneas.
FF 1.9% / 00 12.1% — firmware denso, sin huecos FF grandes (settings/presets probablemente en EEPROM 2K, no en Flash libre).

## Vector table (LE32, +1=Thumb)
- [0]=0x20008000 SP (tope RAM HIGH, válido K20 64K).
- [1]=0x1BD Reset_Handler (código en 0x1B0-0x1C0, validado capstone).
- [2]=0x800D NMI/HardFault? [3..10]=0x7FC5 DefaultHandler, [11]=0x800D, [12]=0x800D, [13]=0x7FC5, [14]=0x87B9 SVC?, [15]=0x8A09 PendSV/SysTick?
- [40]=0x6225 [41]=0x67D5 [61]=0x8B4D [63]=0x8C79, resto 0x800D. K20 IRQ numbers: hay que mapear con RefMan (PITx, FTM, I2C0/1, SPI0, USB, PORTx, ADC, DAC, TSI).
- Cola 0xB51C-0xB9EC: 352B a 00 + tabla punteros 0x1FFF95xx/0x1FFF96xx/97/98/99 paso +8 — muy probable tabla notas/seq/estado (1FFF8000 = base RAM LOW). ¡Punto caliente para presets/escalas!

## Entry points disasm (capstone, ver tools/disasm.py)
- Reset 0x1BC: init stack/clocks (MCG/OSC 16MHz->72MHz), copia .data, zero .bss, `SystemInit`, luego `main`. A desmontar completo en Ghidra.
- 0x800C: loop infinito / Default (strh infinito?).
- 0x87B8/0x8A09: handlers RTOS-less (SVC/PendSV o FTM/PIT tick para clock/divider/portamento).
- 0x6224/0x67D4: lógica grande con `ldrb/strb + cmp #1/#2/#3/#4 + beq.w` — ¡state machine de MODO/SEQ! Offsets struct +0x4BD/+0x4C6/+0x4AC/+0x4B0/+0x274/+0x278 sugieren struct global settings en RAM (~0x1FFFxxxx). Prioridad Ghidra #1.
- 0x8B4C/0x8C78: otro handler (¿USB/MIDI o PIT?).

## Periféricos tocados (literals 0x400xxxxx en pools)
- PORTA-E 0x40049000-0x4004D000 + GPIO 0x400FF000 (pool 0xA1xx): ENC_A/B/S, CLOCK, SS_MATRIX, LEDs, IRQ.
- SPI0 0x4002C000 (0xABC4): DAC8560 + 74HC595 (MOSI=11/SCK=13/CS=10).
- I2C0 0x40066000 + I2C1 0x40067000 (pools 0xACxx/0xAE68): MPR121 touch (SDA=18/SCL=19/IRQ=20). ¿Por qué I2C1 también? ¿2º MPR/expander o solo init genérico Teensyduino? A trazar XREF.
- ADC (pots P/C 22/23), DAC0 0x400CC000? (pressure A14), FTM/PIT (clock/div/portamento), USB0 0x40072000 (Teensy USB-MIDI/Serial? strings no ASCII claros — puede ser USB-MIDI con descriptores binarios).
- SIM 0x40047000 clock gating, TSI 0x40045000 (¿sin usar? touch es via MPR121 externo).

## Strings
331 secuencias >=5 pero ofuscadas/binarias (`pZppG...`, `|vpjd^XRLF@:4...`) — sugiere tablas de notas/escalas comprimidas o fuentes LED, no texto USB. Descriptores USB/MIDI en binario a parsear con `lsusb` dump o Ghidra (buscar `0x40072000` XREF + tabla endpoint).

## Huecos / parche
- ¡Sin gaps FF en Flash app! Parche mínimo requerirá: reclamar cola 0xB9F8-0x3FFFF (209KB libres, fuera del HEX actual — ¡ojo! ¿protegidos o solo no usados? Teensy Loader flashea solo páginas del HEX, resto queda FF → ideal para hook/trampolín), o compactar, o usar EEPROM.
- Estrategia no destructiva propuesta: hook en Reset/main o en handler modo (0x67D4) con `BL` a zona alta libre + `BX LR` de retorno, manteniendo HalfKay + USB. Validar con QEMU Cortex-M4 o Teensy de pruebas antes de hardware real.

## Siguiente paso (a tu decisión de funcionalidad)
1. Cargar `firmware.bin` en Ghidra base 0x0, Thumb, crear `Reset`, etiquetar `DefaultHandler 0x7FC4`, ISRs, pools PORT/SPI/I2C.
2. Nombrar struct settings (offsets 0x274/0x278/0x4AC/0x4BD...), tablas escalas (cola 0xB5xx + `pZppG`), drivers MPR121 (0x5A), DAC8560, 595, ADC, PIT divider, EEPROM presets/calib.
3. Trazar `main loop`: scan touch -> quantize -> DAC CV + gate + pressure + LEDs + USB.
4. Con eso te propongo puntos de parche por funcionalidad/bug que elijas.

Ver: `tools/hex_analysis.py`, `tools/disasm.py`, `docs/raw/firmware.lst`, `docs/01-funcional-manual.md`, `docs/02-hardware-mapa.md`.
