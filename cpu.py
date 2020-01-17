from memory import Memory
from alu import ALU
m = Memory(100)
m.put(ALU.int_to_n_bit_binary(10, 32), ALU.int_to_n_bit_binary(-128, 8))
print(m.at(ALU.int_to_n_bit_binary(10, 32)))