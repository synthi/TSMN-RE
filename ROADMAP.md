# TSNM-RE — Mapa objetivo por fases

Objetivo: portar funciones mkII v4.1/v5.0 a hardware mkI v2.0 (Teensy 3.2) solo con firmware. Sin rework. Sin fallos.

Base ya verificada 09/10/2026: todo Teensy 3.2 (mkI y mkII THT, no existe 3.1), pinout a 300dpi en `docs/img/*_crop.png`.

## Fase 0 — Orientarse (30 min)
1. Leer `docs/01-funcional-manual.md` (qué hace v3.0).
2. Leer `docs/02-hardware-mapa.md` tabla Teensy (qué pines existen de verdad).
3. Leer `docs/05-comparativa-evolucion.md` + `05b-mkii-hardware.md` + `05c-propuestas-portables.md` (qué cambia y qué es portable).
4. Hojear `docs/raw/guide.txt`, `fw41.txt`, `fw50.txt` solo para contexto.
Salida: sabes que mkI = 10 plates + 1 PULSE + pots P/C, mkII = 12 plates + 2 PULSE + botones + menús.

## Fase 1 — Verdad hardware (no tocar FW sin esto)
- Fuente: `02-hardware-mapa.md` + `TSNM_4U_v20_SCHEMATIC.pdf` + `docs/img/mk1_teensy_crop.png` vs `mkii_teensy_crop.png`.
- Claves mkI: 0=ENC_B,1=ENC_A,2=ENC_S,3=CLOCK(Q1),4/5=PULSE diferencial,10/11/13=SPI DAC+595,17=SS_MATRIX,16=2ND_CHAR,18/19/20=MPR121,21=P-POT,22=C-POT,23=NC,A14=PRESSURE.
- Claves mkII: ENC invertido (0=A,1=B), 3=MATRIX1C1,4=DISPLAY_SS,5=B1,6=LED1,7=B2,8=LED2,9=DAC_SS,14=GATE_2,15=GATE_1,20=RESET,21=CLOCK.
- Regla: lo que pide pin 6-9, 14-15, 20-21 distintos o 12 plates o 2º gate o RESET_IN = NO portable sin rework.
Salida: cualquier propuesta pasa el filtro HW antes de codificarse.

## Fase 2 — Verdad funcional v3.0 vs v4.1/v5.0
- Fuente: `01` + `05` + manuales en `tsnm m2 reference/tsnm_firmware_manual_T4_v41.pdf` (31p) y `TSNM_v50_firmware_manual.pdf` (5p).
- v3.0: 19 presets, 20 escalas fijas, transpose ±24, clock+div /1../32.
- v4.1: 17 presets, clock 30-300 + MULT/DIV por arp/seq, arp+seq mejorados, pressure EG, 20+8 escalas user, porta/vibrato con formas, calib 1/1.2/2V.
- v5.0: +USB-MIDI, sin LIVE, clock dedicado, pressure multitouch.
Salida: lista cerrada de qué portar (ver `05c`).

## Fase 3 — Mapa binario (dónde está cada cosa)
- Fuente: `docs/03-toolchain.md` + `04-mapa-firmware.md` + `tools/hex_analysis.py`, `disasm.py`, `mkii_map.py`.
- v3.0: `TSNM_4U_v30.hex` 47608B, 0x0-0xB9F7, libre ~210K. v5.0: LO 64K lleno + HI 14K, total 79540B.
- Pasos: `python3 tools/hex_analysis.py` → vectores/SP 0x20008000/Reset 0x1BD → `arm-none-eabi-objdump` → Ghidra base 0x0 Thumb → marcar PORT/SPI0/I2C0/ADC/DAC/PIT + struct settings + tablas escalas + drivers MPR121(0x5A)/DAC8560/595.
Salida: XREF main-loop (touch→quant→CV/gate/pressure/LED) + puntos de hook en zona libre 0xBA00+.

## Fase 4 — Port solo-FW (en este orden)
- Fuente: `05c-propuestas-portables.md`.
- P0 (días, sin romper UX): transpose ±36, mult/div por ARP/SEQ, ratchet/gate por paso, porta lin/exp/log, vibrato básico, 8 escalas user en EEPROM, undo+overdub.
- P1 (semanas): rhythm ARP 16p, pressure AD/ASR/loop EG, 2º volt-seq en pressure, transpose por presión, vibrato 4 waves, 2ª voz en pressure (avisar: 12-bit).
- No hacer: 12 plates, PULSE2, RESET_IN, pots→menú (salvo reasignar P/C por SW), OLED T12.
Salida: hook no destructivo en Flash libre + HalfKay intacto, probar en Teensy de pruebas antes del módulo.

## Fase 5 — Validación cero-fallos
1. Buscar `3.1` en docs = 0 (solo vale `teensy31` como nombre de placa PIO que cubre 3.2).
2. Tablas 02/05b coinciden con crops. Calibrar 1V y 1.2V por separado + PRESSURE BOTTOM 17 / TOP 65.
3. MPR: si Geiger → bajar SENS / subir DEBOUNCE, si sigue → cambiar placa blue (ver BUILD_NOTES). Cortar VIN-VUSB.
4. Flashear con Teensy Loader 1.33+, verificar presets persisten tras reboot.

## Comandos
```bash
python3 tools/hex_analysis.py
python3 tools/mkii_map.py
pdftotext -layout in.pdf docs/raw/x.txt
mutool draw -r 300 -o docs/img/schematic.png TSNM_4U_v20_SCHEMATIC.pdf
arm-none-eabi-objdump -m arm -M force-thumb -b binary --adjust-vma=0x0 -D docs/raw/firmware.bin > docs/raw/firmware.lst
```
