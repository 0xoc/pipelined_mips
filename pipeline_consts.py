from alu import ALU
from decs import WORD

"""
    pipe line registers
"""


def validate_n_bit_tuple(c, n):
    if not (type(c) == tuple and len(c) == n):
        raise Exception("Invalid %d bit tuple" % n)


def validate_word_tuple(c):
    validate_n_bit_tuple(c, WORD)


class IF_ID:

    def __init__(self):
        self.pc = ALU.int_to_n_bit_binary(0)
        self.inst = ALU.int_to_n_bit_binary(-1)

    def set_pc(self, pc):
        validate_word_tuple(pc)

        self.pc = pc

    def set_inst(self, inst):
        validate_word_tuple(inst)
        self.inst = inst


class ID_EX:

    def __init__(self):
        self.pc = ALU.int_to_n_bit_binary(0)
        self.rd1 = ALU.int_to_n_bit_binary(0)
        self.rd2 = ALU.int_to_n_bit_binary(0)
        self.inst_15_0 = ALU.int_to_n_bit_binary(0, 16)
        self.inst_20_16 = ALU.int_to_n_bit_binary(0, 5)
        self.inst_15_11 = ALU.int_to_n_bit_binary(0, 5)

    def set_pc(self, pc):
        validate_word_tuple(pc)
        self.pc = pc

    def set_rd1(self, rd1):
        validate_word_tuple(rd1)
        self.rd1 = rd1

    def set_rd2(self, rd2):
        validate_word_tuple(rd2)
        self.rd2 = rd2

    def set_inst_15_0(self, i):
        validate_n_bit_tuple(i, WORD)
        self.inst_15_0 = i

    def set_inst_20_16(self, i):
        validate_n_bit_tuple(i, 5)
        self.inst_20_16 = i

    def set_inst_15_11(self, i):
        validate_n_bit_tuple(i,5)
        self.inst_15_11 = i

class EX_MEM:
    JUMP_TARGET = ALU.int_to_n_bit_binary(0, 5)
    ALU_ZERO_FLAG = ALU.int_to_n_bit_binary(1, 5)
    ALU_RESULT = ALU.int_to_n_bit_binary(2, 5)
    RD2 = ALU.int_to_n_bit_binary(3, 5)
    REG_DEST = ALU.int_to_n_bit_binary(4, 5)


class MEM_WB:
    ALU_RESULT = ALU.int_to_n_bit_binary(0, 5)
    READ_DATA = ALU.int_to_n_bit_binary(1, 5)
    REG_DEST = ALU.int_to_n_bit_binary(2, 5)


"""
    pipe line controls
"""


class WB_CONTROL:

    def __init__(self):
        self.MemToReg = 0
        self.RegWrite = 0


class MEM_CONTROL:

    def __init__(self):
        self.Branch = 0
        self.MemRead = 0
        self.MemWrite = 0


class EX_CONTROL:

    def __init__(self):
        self.ALUSource = 'rs'
        self.RegDst = 'rd'
        self.ALUOp = '00'
