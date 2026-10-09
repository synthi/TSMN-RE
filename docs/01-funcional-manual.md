# M1 — TSNM 4U v3.0 Manual funcional (extraído de TSNM_4U_v30_guide.pdf, 6 pág A4, InDesign CC 2018)

Fuente raw: `docs/raw/guide.txt`. Esquema v2.0 + firmware `TSNM_4U_v30.hex` (46.5KB).

## Panel / IO
- NOTE CV OUT >7 octavas, PULSE OUT, PRESSURE OUT 0-10V, CLOCK IN.
- Pots: "P" PORTAMENTO (glide), "C" CLOCK (rate interno; a tope CCW = espera clock externo).
- Encoder con switch: 1s entra/sale SETTINGS; en ARP = LATCH; en SEQ = RESET.
- Placas: 10x NOTE + 2x TRANSPOSE (izq/der).

## Edición directa
- Transpose: hold plate + encoder = -24..+24 semitonos.
- Note: hold note + encoder = tune CV cuantizado a semitono, rango 3 octavas.

## MODES: KEYBOARD / ARPEGGIATOR / SEQUENCER

### Común SEQ (solo SEQ/ARP)
- SEQ DIRECTION: UP/DOWN/PING-PONG/RANDOM
- LENGTH 1..32, EDITOR (scroll steps, hold L-trans+enc=nota, hold R-trans+enc=trigger, hold ambas+enc=len L1-L8), LEARN (toca plates=entra seq, L-trans=step len, R-trans=trig on/off, enc=undo sin redo, press enc=exit), RESET SOURCE: FREE RUNNER/TOUCH PLATES/CLOCK, loop overdub al tocar plate (bloqueable).
- RANDOM NOTE: hold R-trans+enc = scope 1-30, hold L-trans+enc = probabilidad 0-35.

### Solo ARP
- ARP DIRECTION: UP/DOWN/... (ver p3), ARP VARIATOR: hold L-trans+enc añade notas +5st al patrón. Ej x2 sin var: C1-E1-G1; !2 con var: C1-F1-A#1-E1-A1-D2-G1-C2-F2; >2 variaciones al final.
- Orden: por número de placa #01..#10, no cromático. Tras SETTINGS, press enc = HOLD.
- PRESSURE MODE / RISE / FALL (ver p3).

### Solo SEQ
- Tras SETTINGS, press enc = RESET a paso 1. Transposición por note plates + quantize opcional.

## Quantizer / escalas (p3)
- OFF semitones + ionian dorian phrygian lydian mixolydian aeolian locrian b+bluesMaj b-bluesmin p+pentMaj p-pentmin folk japanese gamelan gypsy arabian flamenco whole quarter.
- FILL SCALE: hold L-trans + press enc 1s rellena plates con escala. ROOT: hold R-trans+enc.

## Transpose mode / plate values / pulse / voltage / clock div
- TRANSPOSE MODE: LATCHING / LATCHING IMMEDIATE / MOMENTARY.
- PLATE VALUES: hold + enc -24..+24st (reescribe tune 3 oct).
- PULSE MODE: TRANSIENT(trigger)/SUSTAINED(gate).
- VOLTAGE MODE: 1.2V/oct Buchla vs 1V/oct. ¡Calibrar por separado!
- CLOCK DIVIDER: /1../32 sobre CLOCK IN.

## Pressure
- PRESSURE BOTTOM/TOP: patch PRESSURE OUT a param audible, dedo en plate + variar apoyo, hold trans+enc ajusta. Defaults 17 / 65.

## Presets (19)
- Guarda layout + settings. Al boot carga último. Enc scroll, hold L-trans + press enc 1s = LOAD, mismo gesto = SAVE (según selección).

## Calibration
- Hold enc 1s, multímetro a NOTE CV, scroll octavas con enc, hold trans+enc para trim. Hacer para 1.2V y 1V por separado. Hold enc 1s: SAVE?/INIT?/EXIT?

## Sensitivity / Debounce (MPR121)
- Síntoma Geiger = bajar SENS / subir DEBOUNCE. Hold enc en power-on, rotar valor, press enc = siguiente param. Tercer param = encoder direction. Luego reboot power-cycle. Mantener SENS alta / DEBOUNCE bajo si se puede.

## Implicaciones reversing
- Todo este árbol de menus/settings/presets/calibración vive en Flash (46KB) + EEPROM 2K (presets/calib). Buscar: tablas escalas (~20), state machine modo, handler encoder (hold 1s), I2C MPR121, SPI DAC8560, ADC pots, PIT clock/divider, GPIO pulse/gate.
- Siguiente: cruzar cada item con dirección Flash/RAM en `04-mapa-firmware.md`.
