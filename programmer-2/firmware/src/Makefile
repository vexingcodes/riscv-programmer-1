OUT ?= /out

.PHONY: all
all: $(OUT)/code.txt

.PHONY: clean
clean:
	rm $(OUT)/code.o $(OUT)/code.bin $(OUT)/code.txt

$(OUT)/code.o: code.S
	riscv64-linux-gnu-gcc -nostdlib -march=rv32i -mabi=ilp32 code.S -o $(OUT)/code.o

$(OUT)/code.bin: $(OUT)/code.o
	riscv64-linux-gnu-objcopy --dump-section .text=$(OUT)/code.bin $(OUT)/code.o

$(OUT)/code.txt: $(OUT)/code.bin
	bash -c "paste -d'#' \
	  <(xxd -b -c 4 $(OUT)/code.bin | cut -c11-46) \
	  <(riscv64-linux-gnu-objdump -b binary -m riscv:rv32 -D -EL $(OUT)/code.bin | tail -n +8)" \
	  > $(OUT)/code.txt
