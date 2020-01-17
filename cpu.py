from memory import Memory
from alu import ALU
from decs import BYTE_SIZE, WORD

alu = ALU()
instruction_memory = Memory(1024)
data_memory = Memory(1024)

a = 45
b = -46

data_memory.put(ALU.int_to_n_bit_binary(32),
      alu.exc(alu.int_to_n_bit_binary(a), alu.int_to_n_bit_binary(b), '00')
      )
print(ALU.n_bit_binary_to_decimal(data_memory.at(ALU.int_to_n_bit_binary(32, data_memory.addr_size))))
