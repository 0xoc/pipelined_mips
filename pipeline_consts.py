from alu import ALU

"""
    pipe line registers
"""


class IF_ID:
    PC = ALU.int_to_n_bit_binary(0, 5)
    INST = ALU.int_to_n_bit_binary(1, 5)


class ID_EX:
    PC = ALU.int_to_n_bit_binary(0, 5)
    RD1 = ALU.int_to_n_bit_binary(1, 5)
    RD2 = ALU.int_to_n_bit_binary(2, 5)
    INST_15_0 = ALU.int_to_n_bit_binary(3, 5)
    INST_20_16 = ALU.int_to_n_bit_binary(4, 5)
    INST_15_11 = ALU.int_to_n_bit_binary(5, 5)


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
        self.ALUSource = ALU.int_to_n_bit_binary(0)
        self.RegDst = ALU.int_to_n_bit_binary(0, 5)
        self.ALUOp = '00'
