# M2 — Mapa hardware TSNM 4U v2.0 (verificado crop 300dpi) + BUILD_NOTES

Imagen: `docs/img/schematic.png` + crop alta-res `docs/img/mk1_teensy_crop.png`. Raw montaje: `docs/raw/build_notes.txt`.
**Hardware 100% Teensy 3.2 en mkI y mkII THT (BOM mkII: no funciona con Teensy 4.0). Pinout verificado a 300dpi 09/10/2026.**

## Teensy 3.2 -> nets mkI (verificado crop `docs/img/mk1_teensy_crop.png` + imagen usuario)
| Teensy | Label esquema | Destino | Notas mkII THT (`docs/img/mkii_teensy_crop.png`) |
|---|---|---|---|
| 0 | ENC_B | encoder B via 510R+C100nF | mkII: 0=ENC_A (invertido) |
| 1 | ENC_A | encoder A idem | mkII: 1=ENC_B |
| 2 | ENC_S | encoder SW via 510R | igual mkII: 2=ENC_S |
| 3 | CLOCK | CLOCK_IN jack -> R11 100k -> Q1 MMBT3904 -> pin 3 | mkII: 3=MATRIX1C1. CLOCK pasa a 21/A7 |
| 4 | LOW_PIN | TL072 IC1A + divisor -> PULSE_OUT J1-1 | UN solo PULSE_OUT diferencial HI+LOW. mkII: 4=DISPLAY_SS |
| 5 | HI_PIN | idem complementario | mkII: 5=BUTTON_1 |
| 6 | NC | rayita sin net | mkII: 6=LED_1 |
| 7 | NC | rayita sin net | mkII: 7=BUTTON_2 |
| 8 | NC | rayita sin net | mkII: 8=LED_2 |
| 9 | NC | rayita sin net | mkII: 9=DAC_SS |
| 10/CS | SS_DAC | DAC8560 SYNC | SPI0 CS DAC. mkII: 10=NC |
| 11/DOUT | MOSI | DAC8560 DIN + 74HC595 DS | SPI0 MOSI. mkII: 11=SPI_MOSI |
| 12/DIN | NC | rayita sin net, MISO sin usar | igual mkII: 12=NC |
| 13/SCK | SCLK | DAC8560 SCLK + 74HC595 SH_CP | SPI0 SCK. mkII: 13=SPI_SCK |
| 14/A0 | LED1 | LED1 via R30 1k8 | mkII: 14=GATE_2 (ojo: en TEENSY3.2 impreso A0=14 lleva GATE_2) |
| 15/A1 | LED2 | LED2 via R31 1k8 | mkII: 15=GATE_1 (A1=15 lleva GATE_1) |
| 16/A2 | 2ND_CHAR_PIN | MATRIX2 C5 via R32 1k, enable 2o char | mkII: 16=test `16` |
| 17/A3 | SS_MATRIX | IC3+IC4 595 ST_CP latch | CS matrices. mkII: 17=test `17` |
| 18/A4/SDA0 | MPR121_SDA | MPR121 SDA | I2C0. mkII: 18=I2C_SDA igual |
| 19/A5/SCL0 | MPR121_SCL | MPR121 SCL | I2C0. mkII: 19=I2C_SCL igual |
| 20/A6 | MPR121_IRQ | MPR121 IRQ | mkII: 20=RESET_EXT |
| 21/A7 | PORTAMENTO_POT | pot P 1k a +3V3 | mkII: 21=CLOCK_EXT |
| 22/A8 | CLOCK_POT | pot C 1k a +3V3 | mkII: 22=NC (`22`) |
| 23/A9 | NC | rayita corta flotante | mkII: 23=NC (`23`) |
| A14/DAC | PRESSURE | DAC K20 -> R6 1k -> TL072 IC1B x3 -> R7 1k -> PRESSURE_OUT 0-10V | igual mkII (TL074+filtrado) |
| VIN | +5V | LM1117 +5V | cortar traza VIN-VUSB. mkII: VIN=5V igual |
| AGND/3.3V/GND | +3V3/GND | ADP150 +3V3_DAC, MPR121, 595 | igual mkII |

Pots P/C: 1k a +3V3 + 100nF a GND. Encoder SW1: A/B/S con RC.

## MPR121 breakout (12ch capacitivo, I2C0: SDA 18 / SCL 19 / IRQ 20)
- Board externa en sockets: 3V3/GND/SDA/SCL/IRQ/ADD. ADD define addr (def 0x5A).
- Electrodos 0..11 -> 10 note plates + 2 transpose plates. Pads abajo (0-11 + X).
- J4 expander: pines 5=SDA 7=SCL 9=+3V3.
- Blue boards rinden mejor que black segun BUILD_NOTES. Si aun calibrado va raro, probar otro proveedor. SENS/DEBOUNCE se ajustan en firmware (hold enc en power-on): bajar SENS / subir DEBOUNCE solo si hay falsos toques. Mantener SENS alta / DEBOUNCE bajo si se puede.

## DAC + CV NOTE (precisión)
- **IC2 DAC8560 16-bit SPI VSSOP-8**: SYNC=SS_DAC(10), SCLK=13, DIN=11(MOSI), VOUT->R13 27k 0.1% -> OPA171 IC5 (+10.5V rail, gain con R1 100k 0.1%/R14 33k 0.1%/R15 100k 0.1%) -> R2 1k 0.1% -> NOTE_OUT. Refs: R1/R2/R13/R14/R15 0.1% críticos (BUILD_NOTES: soldar primero).
- Calib 1.2V/oct y 1V/oct por separado = 2 juegos coeficientes en EEPROM.
- Rango >7 octavas NOTE CV (manual) => ~8.4V @1.2V/oct.

## Pressure / Pulse analógico
- PRESSURE: DAC interno A14 -> R6 1k -> TL072 IC1B (G=3: 10k/20k) -> R7 1k -> PRESSURE_OUT 0-10V. PRS test point.
- PULSE (HI/LOW_PIN): TL072 IC1A comparador/divisor 4k7 -> R4 1k -> PULSE_OUT. TRANSIENT vs SUSTAINED = ancho pulso por firmware.

## LEDs matrices (2x 74HC595 cascada SPI: MOSI 11 + SCLK 13 + ST_CP 17)
- IC3+IC4 74HC595: DS=MOSI(11), SH_CP=SCLK(13), ST_CP=SS_MATRIX(17/A3). Q0-Q7 -> filas/columnas MATRIX1 KWM-20571XSB + MATRIX2 KWM-20571XSB via R17-R24 100R + R32/R33 1k (2ND_CHAR_PIN 16/A2 = enable 2o char, a MATRIX2 C5).
- MATRIX1: C1-C4/Q + R1-R7. MATRIX2: C1-C5/R1-R7. Matrices: LTP-747KR (der), TA07-11SURKWA (izq), KWM-20571CSB (izq) — orientar textos según BUILD_NOTES.
- Firmware: bitbang/SPI a ~MHz, latch por frame, multiplex para modos/settings/seq steps.

## Clock in
- CLOCK_IN jack -> R11 100k -> Q1 MMBT3904 (inversor) -> R10 220k -> CLOCK (Teensy 3.2 pin 3). Divider /1../32 en firmware (cuenta flancos). LED1/LED2 via R30/R31 1k8.

## Alimentación
- Eurorack +15/-15/GND (+5V opcional SP1). D1/D2 protección, C19/C20 47u/25V. LM1117 +15V->+5V (C21 33u, L1 bead, C22/C23 100n), ADP150 IC7 +5V->+3V3_DAC (C16 10u). +3V3 para Teensy/MPR/595. OPA rail -15V/+15V? IC5 -15V/+15V? TL072 +/-15V. Chequear 3V3_DAC limpio para DAC8560 VDD/VREF.
- Cortar VIN-VUSB en Teensy (BUILD_NOTES) para no backpower USB+rack.

## Conectores
- J1: 1=PULSE_OUT 2=NOTE_OUT. J2: 1=CLOCK_IN 2=PRESSURE_OUT. J4 EXP: MPR SDA/SCL/+3V3. 16-pin SMD header panel. Bananas (4U Buchla).

## Cruce firmware (para 04-mapa)
- I2C0 0x40066000 (pool 0xACxx) = MPR121. SPI0 0x4002C000 (0xABC4) = DAC8560+595. PORTx 0x40049..0x4004D (pool 0xA1xx) = ENC/CLOCK/LED/SS. ADC pots en 22/23, DAC interno pressure. PIT/FTM clock/divider. EEPROM presets/calib.

## Dudas cerradas 09/10/2026 (verificado crops + imagen usuario)
1. ST_CP/Latch matrices = SS_MATRIX 17/A3. Cerrado.
2. 2ND_CHAR_PIN = 16/A2, enable 2o char a MATRIX2 C5 via R32. Cerrado.
3. 21/A7 = PORTAMENTO_POT, 22/A8 = CLOCK_POT, 23/A9 = NC flotante. Cerrado.
4. HI/LOW_PIN 4/5 = UN solo PULSE_OUT diferencial (no 2 salidas). TRANSIENT/SUSTAINED = FW. Cerrado.
5. Teensy = 3.2 en mkI y mkII THT (BOM mkII: "TSNM will not work with Teensy 4.0!"). MPR blue rinde mejor que black pero SENS/DEBOUNCE lo compensan; defaults: ver guide (PRESSURE BOTTOM 17 / TOP 65). Cerrado.
