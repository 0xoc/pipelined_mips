import tests

from alu import ALU
from cpu import CPU

program = open("program.inst")
instructions = program.readlines()

cpu = CPU()

cpu.load_instructions(instructions)

cpu._instruction_memory.set_mem_read(True)

print(cpu.fetch())
print(cpu.fetch())