# M3 — Toolchain desensamble MK20DX256 + entorno macOS (esta máquina)

## Instalado hoy (brew+pip, Apple Silicon macOS Tahoe)
- `poppler 26.10.0` (`pdftotext/pdfinfo`), `mupdf-tools 1.28.5` (`mutool draw`), `arm-none-eabi-gcc 16.2.0` (incluye `objdump/objcopy/nm/size/gdb`).
- Python 3.9: `pypdf pdfminer.six pymupdf Pillow intelhex capstone pyelftools`.
- Verificado: `which pdftotext pdfinfo mutool arm-none-eabi-objdump/objcopy/gcc` + `py-ok`.

## Pendiente recomendado (no instalado aún)
- Ghidra (Temurin JDK + GhidraARM + SVD K20DX256) o Rizin/Cutter + ImHex para estático visual.
- Teensy Loader 1.33+ / TyTools (`tycmd`) para flashear+monitor, J-Link/OpenOCD+SWD para debug, Saleae Logic para I2C/SPI.
- Arduino CLI + Teensyduino o PlatformIO `teensy@3.2` (board `teensy31` cubre 3.2, mismo MK20DX256VLH7) para rewrite limpio.
- SVD NXP `MK20DX256xxx7.xml` para nombrar registros.

## Recetas usadas
```bash
pdftotext -layout in.pdf docs/raw/x.txt
mutool draw -r 300 -o docs/img/schematic.png TSNM_4U_v20_SCHEMATIC.pdf
python3 tools/hex_analysis.py   # HEX->BIN + vectores + strings + pools 0x400xxxxx
python3 tools/disasm.py         # capstone Thumb entry points
arm-none-eabi-objdump -m arm -M force-thumb -b binary --adjust-vma=0x0 -D docs/raw/firmware.bin > docs/raw/firmware.lst
arm-none-eabi-objcopy -I ihex TSNM_4U_v30.hex -O binary docs/raw/firmware.bin  # alternativa
arm-none-eabi-nm / size / strings / entropy sobre BIN
```

## Notas K20 / Teensy
- Flash 0x00000000-0x0003FFFF (256K), RAM LOW 0x1FFF8000-FFFFFFFF + HIGH 0x20000000-0x20007FFF (2x32K), SP init 0x20008000.
- Bootloader HalfKay en MKL02Z32 externo (EZPort) — no ocupa Flash app. Para re-flash: botón Program + Teensy Loader.
- Entradas 5V-tolerant salvo A10-A14/AREF/Program/Reset. DAC interno A14 = pressure.
