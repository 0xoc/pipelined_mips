from alu import ALU
from decs import WORD


class RegisterFile:

    def __init__(self, register_size=WORD, count=32):
        self.register_size = WORD
        self.count = count
        self.data = {}

        # initialize registers
        for i in range(self.count):
            self.data[ALU.int_to_n_bit_binary(i,5)] = ALU.int_to_n_bit_binary(0, WORD)

