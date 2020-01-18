import tests

from alu import ALU
from cpu import CPU

program = open("program.inst")
instructions = program.readlines()

cpu = CPU()

cpu.load_instructions(instructions)

cpu._instruction_memory.set_mem_read(True)

cpu._register_file.set_register_write(True)
cpu._register_file.set_write_r(ALU.int_to_n_bit_binary(5, 5))
cpu._register_file.set_write_data(ALU.int_to_n_bit_binary(3))
cpu._register_file.set_register_write(False)

cpu._register_file.set_register_write(True)
cpu._register_file.set_write_r(ALU.int_to_n_bit_binary(7, 5))
cpu._register_file.set_write_data(ALU.int_to_n_bit_binary(10))
cpu._register_file.set_register_write(False)

while cpu.fetch():
    cpu.decode()
    print(cpu.execute())