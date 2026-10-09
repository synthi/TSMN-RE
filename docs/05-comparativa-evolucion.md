# 05 — Comparativa TSNM 4U v3.0 vs mkII v4.1/v5.0 (verificado manuales reales + esquemas alta-res)

Base: v3.0 (Teensy 3.2) + `tsnm m2 reference/` (mkII v5.0 Teensy 3.2) + manuales `tsnm_firmware_manual_T4_v41.pdf` (31p, 17-01-2023) + `TSNM_v50_firmware_manual.pdf` (5p, 13-06-2023).
T12: solo inspiración (OLED+otra CPU, no portable binario/HW).
**Hardware 100% Teensy 3.2 en mkI y mkII THT. Pinout verificado a 300dpi 09/10/2026.**

## A. Firmwares: v3.0 vs v5.0 (medido aquí + manuales)
- v3.0: 47608 B, un banco 0x00000000-0x0000B9F7. Libre hasta 256K: ~214K.
  Manual 2017 (6p A4): 19 presets, 20 escalas fijas, pots P/C físicos, 1x PULSE (TRANSIENT/SUSTAINED), 1V/1.2V oct, CLOCK_IN + divider /1../32, transpose táctil ±24.
- v4.1 (manual T4 31p, 2023-01-17): 11 grupos settings (LIVE, KEYBOARD&ARP, SEQUENCER, PRESSURE, QUANTIZER, PORTAMENTO, VIBRATO, GATE&TRIGGER, INTERNAL CLOCK, PRESETS, CALIBRATION), 17 presets, transpose botones ±36, internal clock 30-300BPM con MULT/DIV ÷32..×8 por arp/seq por separado, arp VARIATOR x1-x5 + intervalo 1-12st + 3 comportamientos (off/end/each) + RHYTHM 16 pasos + GATE LENGTH 1-99%, seq 8 melodías x 32 pasos + overdub + GATE PRESSURE + CV modes SEQ/FREE/RANDOM/PRESS + SEQ RATE 1-8 + LEN 1-8, pressure AD/ASR/loop EG (ATK/DEC-REL 8-2000ms x1/x2/x3 + shapes LIN/EXP/LOG + modulación por presión 0-9) + PRESSURE RECORDER (loop/1-shot/overdub), quantizer 20 escalas + 8 USER (16 notas c/u) + ROOT, portamento TIME/SHAPE/MODE, vibrato 12 waves + AMOUNT/SPEED/SHAPE por presión, gate/trigger sources (off-on/seq/arp/pressure/random-gate/clock x4/x2 + NOT+AND condicionantes), calib NOTE 0/2/5/8V + PRESSURE + 1V/1.2V/2V oct + PRESSURE BOTTOM/TOP + VREF IN/EX (solo T4).
- v5.0 (delta 5p, 2023-06-13, sobre v4.1): +USB MIDI in/out, bugfix arp/seq reset + non-1V/oct en T4 + pitch-shift al salir de SEQ REC, **elimina LIVE functions** (confusas), clock dedicado en settings (sin combos), pressure escanea TODAS las teclas a la vez (antes solo última activa).
- v5.0 binario (`TSNM_mkII_v50_4U_t32.hex`, 4975 líneas, con `:020000021000EC`):
  banco LO 0x00000000-0x0000FFFF (65536 B lleno) + banco HI
  0x00010000-0x000136B3 (14004 B). Total 79540 B. Libre: ~182K.
- Vectores: SP 0x20008000 y Reset 0x000001BD **idénticos** → misma
  raíz de código Teensyduino, evolución por añadidos.
  DefaultHandlers cambian (v3.0 0x800D/0x7FC5, v5.0 0xDDC9/0xDD81):
  el código se ha movido/crecido, no es un parche menor.
- Pools K20: LO v5.0 concentra USB0 0x40072000 (x25), DMA 0x40008000,
  BITBAND 0x4000F000, GPIO, ADC, DAC; HI concentra PORTA-E, I2C0
  0x40066000, I2C1 0x40067000, SPI0 0x4002C000. En v3.0 todo estaba
  junto en 46K. El linker de v5.0 partió drivers a HI.
- Strings HI v5.0 (legibles, no existen en v3.0):
  `TSNM mk2 v50`, `Read as INPUT:`, `Read as INPUT PULLUP:`,
  `SEIODOPHLYMIAELOB+B-P+P-FOJAGAGYARFLWTU1U2U3U4U5U6U7U8`,
  `C C#D D#E F F#G G#A A#H`, charset ASCII completo para matrices.
  → nuevo menú de config de pines, más notas/escalas y fuente display.

<!--PART2-->
