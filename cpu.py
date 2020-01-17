from memory import Memory
from alu import ALU
from decs import BYTE_SIZE, WORD

alu = ALU()
m = Memory(100, WORD)
a = 45
b = -46

m.put(ALU.int_to_n_bit_binary(32, m.addr_size),
      alu.exc(alu.int_to_n_bit_binary(a), alu.int_to_n_bit_binary(b), '00')
      )
print(ALU.n_bit_binary_to_decimal(m.at(ALU.int_to_n_bit_binary(32, m.addr_size))))
