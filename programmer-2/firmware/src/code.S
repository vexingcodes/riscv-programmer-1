.text; .global _start; _start:
li t0, 1
la t1, 2
sw t0, 0(t1)
1: j 1b
