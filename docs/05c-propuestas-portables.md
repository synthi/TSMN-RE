# 05c — Funciones mkII v5.0 / T12 portables a tu TSNM v3.0 (solo FW)

Fuentes: ModularGrid mkII#31766 + T12#49054, lame.buanzo reviews,
repo Overdubbing-Sequencer (3ch alt-FW mkII), strings HI v5.0,
tu manual v3.0.

## mkII v4.0→v5.0 (lista pública, toda portable salvo HW)
- Cadena keyboard>arp>seq>quant>portamento>vibrato.
- Clock interno + mult/div individual arp y seq.
- Transpose por presión (±36 botones en mkII; en ti ±36 por FW).
- Arp mejorado + rhythm seq + gate/ratchet por paso.
- SEQ record con overdub (tu learn es destructivo).
- Pressure como AD/ASR/loop EG + mod interna + 2º volt-sequencer.
- 8 escalas user-editables (tú 20 fijas).
- Portamento shapes. Vibrato 4 waves + depth por presión.
- 2-note poly (NOTE 16-bit + PRESSURE 12-bit como 2ª voz aprox).
- 12 plates 6 oct (tú 10 plates 3 oct) → emular 12 vía banco/octava.
- 17 presets (tú 19) → remapear EEPROM a 17 + 8 escalas.

## T12 (solo ideas, por OLED/CPU nueva)
- Operators (touch/seq/arp como personalidades) + CV shaping común
  (quant/vibrato/portamento) + CV generators extra + mod externa de
  sus propios parámetros. Portable como: 2 operators compuestos
  (SEQ+ARP paralelo, TOUCH→EG+SEQ) + matriz mod 4x4
  (pressure/clock/step → EG/vibrato/porta/div).

## Propuestas P0 (días, hook en 0xBA00+ de tu Flash, sin romper UX)
1. Transpose ±36. 2. Mult/div por ARP y SEQ. 3. Ratchet/gate por
   paso. 4. Portamento shapes lin/exp/log. 5. Vibrato básico.
   6. 8 escalas user en EEPROM. 7. Undo + overdub no destructivo.

## Propuestas P1 (semanas, pipeline estilo mkII)
8. Rhythm ARP 16p. 9. Pressure AD/ASR/loop EG. 10. 2º volt-seq en
   pressure. 11. Transpose por presión. 12. Vibrato 4 waves + depth
   presión. 13. 2ª voz en pressure (documentar precisión 12-bit).

## No portable sin rework
12 plates físicos, 2 botones iluminados, PULSE2, RESET_IN, pots→menú
(si quieres, reasigna tus pots P/C por software), OLED T12,
polifonía precisa, reguladores mkII.
