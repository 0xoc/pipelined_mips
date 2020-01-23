import tests
from alu import ALU
from cpu import CPU
from tabulate import tabulate

program = open("lw.inst")
mem_file = open("mem.txt", "w")
reg_file = open("reg.txt", "w")
instructions = program.readlines()

cpu = CPU()

cpu.load_instructions(instructions)
register_data = [[i for i in range(32)] + ['clk', ]]

for j in range(50):
    cpu.cycle()

    # save result to file
    mem_file.write("Cycle %d\n " % j)
    reg_data = {}
    for i in range(0, cpu._data_memory.size, 4):
        mem_file.write("[" + str(i) + "]" + " ----> " + str(
            ALU.n_bit_binary_to_decimal(
                tuple(cpu._load_w(cpu._data_memory, ALU.int_to_n_bit_binary(i)))
            )
        ) + "\t")

    register_data += [[str(ALU.n_bit_binary_to_decimal(
        tuple(cpu._register_file.at(ALU.int_to_n_bit_binary(i, 5))))
    ) for i in range(32)] + [str(j)]]

reg_file.write(tabulate(register_data))
