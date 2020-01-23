import tests

from alu import ALU
from cpu import CPU

program = open("lw.inst")
mem_file = open("mem.txt", "w")
reg_file = open("reg.txt", "w")
instructions = program.readlines()

cpu = CPU()

cpu.load_instructions(instructions)

# 00100000000001000000000000000101
# cpu._register_file.put(ALU.int_to_n_bit_binary(4, 5), ALU.int_to_n_bit_binary(5))

for j in range(20):
    cpu.cycle()

    # save result to file
    mem_file.write("Cycle %d\n " % j)
    for i in range(0, cpu._data_memory.size, 4):
        mem_file.write(str(i) + "\t" + str(
            ALU.n_bit_binary_to_decimal(
            tuple(cpu._load_w(cpu._data_memory, ALU.int_to_n_bit_binary(i)))
            )
        ) + "\n")

    reg_file.write("Cycle %d\n " % j)
    for i in range(32):
        reg_file.write(str(i) + "\t" + str(
            ALU.n_bit_binary_to_decimal(
            tuple(cpu._register_file.at(ALU.int_to_n_bit_binary(i, 5)))
            )
        ) + "\n")


