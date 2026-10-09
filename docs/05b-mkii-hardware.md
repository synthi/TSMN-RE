## B. Hardware: v2.0 (tuyo) vs mkII v1.0 THT (medido de esquemas)

Tu v2.0: 10 plates + 2 transpose plates táctiles, 1x PULSE, CLOCK_IN
vía Q1 MMBT3904, TL072+OPA171, LM1117+ADP150, 595 con SS_MATRIX.
mkII v1.0 (`tsnm_4u_mkii_tht_v10_schematic.pdf`, EAGLE 7.3.0, 2023, Teensy 3.2):
12 plates (MPR121 0-11 directos a J7: PLATE_0..PLATE_11) + 2 botones
mecanicos iluminados SW1/SW2 (BUTTON_1 a Teensy 5, BUTTON_2 a Teensy 7,
LED_1 a Teensy 6, LED_2 a Teensy 8), 2x PULSE (GATE_1 a Teensy 15/A1,
GATE_2 a Teensy 14/A0, via TL074), CLOCK a Teensy 21/A7 + RESET a Teensy
20/A6 (Q1/Q2 2N3904), encoder invertido (ENC_A a 0, ENC_B a 1, ENC_S a 2),
2x matrices 5x7 (IC1/IC2 74HC595 DIP con DISPLAY_SS a 4 + MATRIX1C1 a 3), DAC8560 + OPA277 (PITCH, Rs 0.1%:
30k1/33k/100k/1k), TL074 pressure (47k/220p filtro) + gates,
R-78E5.0 DC/DC + 78L33, EDAC Buchla + bananas (PITCH/PRESSURE/
PULSE1/PULSE2/CLOCK/RESET).
Teensy mkII (verificado `docs/img/mkii_teensy_crop.png`, Teensy 3.2): 0 ENC_A, 1 ENC_B, 2 ENC_S, 3 MATRIX1C1, 4 DISPLAY_SS,
5 BUTTON_1, 6 LED_1, 7 BUTTON_2, 8 LED_2, 9 DAC_SS, 10 NC, 11 SPI_MOSI, 12 NC, 13 SPI_SCK,
15/A1 GATE_1, 14/A0 GATE_2, A14 PRESSURE, 18 SDA, 19 SCL, 20 RESET,
21 CLOCK, 22/23 NC como pots (tus pots P/C desaparecen!
portamento/clock pasan a menu).
BOM mkII: 470R/100R/1k/10k/20k/47k/100k + 0.1% 15ppm, 74HC595x2,
DAC8560, OPA277, TL074, 78L33, R-78E5, EN11 encoder, KS01-BL
botones, matrices 5x7 LTP-747KR/FYM..., Teensy 3.2 (¡NO 4.0!),
MPR121 SparkFun-clon o Adafruit.
Conclusión: tu placa no puede dar 12 plates ni 2 gates ni reset-in
sin rework. Todo lo demás es firmware portable.
