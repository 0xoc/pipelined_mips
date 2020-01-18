from memory import Memory
from alu import ALU
from register_file import RegisterFile
from decs import BYTE_SIZE, WORD

rg = RegisterFile()

rg.reg_write = True
rg.set_write_data(ALU.int_to_n_bit_binary(5))

i = 0
for k in rg.data.keys():
      rg.set_write_r(k)
      rg.set_write_data(ALU.int_to_n_bit_binary(-i))

      rg.set_read_r1(k)
      rg.set_read_r2(k)

      if rg.read_d1 == rg.read_d2:
            print(rg.read_d1)

      i += 1
