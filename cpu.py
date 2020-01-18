from decs import BYTE_SIZE, WORD
from memory import Memory
from alu import ALU
from register_file import RegisterFile


class ControlUnit:


class CPU:
    def __init__(self):
        self._instruction_memory = Memory(1024, byte_size=BYTE_SIZE)
        self._data_memory = Memory(1024, byte_size=BYTE_SIZE)
        self._register_file = RegisterFile(1024)
        self._alu = ALU()
        self._pc = ALU.int_to_n_bit_binary(0)

    def fetch(self):
        n = WORD // BYTE_SIZE

        # load n cells from instruction memory
        instruction = []
        for i in range(n):
            pass