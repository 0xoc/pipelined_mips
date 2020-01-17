from memory import Memory
from alu import ALU
m = Memory(100, 4)
# 1 1 1 1
# 1 0 0 0
# 0 1 1 1
m.put(ALU.int_to_n_bit_binary(10, 32), ALU.int_to_n_bit_binary(7, 4))
print(ALU.n_bit_binary_to_decimal(m.at(ALU.int_to_n_bit_binary(10, 32))))