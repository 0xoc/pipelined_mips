import copy

from decs import BYTE_SIZE, WORD
from memory import Memory
from alu import ALU
from register_file import RegisterFile
from pipeline_consts import EX_CONTROL, MEM_CONTROL, WB_CONTROL, IF_ID, ID_EX

FETCH = '0'
DECODE = '1'
EXC = '2'
MEM = '3'
WB = '4'


class ControlUnit:
    pass


class CPU:

    def __init__(self):
        self._instruction_memory = Memory(1024, byte_size=BYTE_SIZE)
        self._data_memory = Memory(1024, byte_size=BYTE_SIZE)
        self._register_file = RegisterFile(32)
        self._alu = ALU()
        self._pc = ALU.int_to_n_bit_binary(0)

        # pipe line registers
        self._if_id = IF_ID()
        self._id_ex = ID_EX()
        self._ex_mem = RegisterFile(count=5)
        self._mem_wb = RegisterFile(count=3)

        # pipe line controls
        self._id_ex_ex_control = EX_CONTROL()
        self._id_ex_mem_control = MEM_CONTROL()
        self._id_ex_wb_control = WB_CONTROL()

        self._ex_mem_wb_control = WB_CONTROL()
        self._ex_mem_m_control = MEM_CONTROL()

        self._mem_wb_wb_control = WB_CONTROL()

    def load_instructions(self, instructions):
        """
        load instructions from an array read from a file
        this is a helper function to initialize the instruction memory
        :param instructions:
        :return:
        """

        memory_cell_size = self._instruction_memory.byte_size

        # times needed to access the memory to fetch one word
        n = WORD // memory_cell_size

        # start putting instruction into memory from address 0
        base_addr = ALU.int_to_n_bit_binary(0)

        self._instruction_memory.set_mem_write(True)

        for j in range(len(instructions)):
            instruction = instructions[j]

            inst = [int(c) for c in instruction.replace('\n', '')]

            for i in range(n):
                # calculate write addr
                self._alu.set_input_1(base_addr)
                self._alu.set_input_2(ALU.int_to_n_bit_binary(i + j * n))
                self._alu.set_op('00')
                addr = self._alu.result

                # write data
                unit_data = tuple(inst[i * memory_cell_size: (i + 1) * memory_cell_size])

                self._instruction_memory.set_write_addr(addr)
                self._instruction_memory.set_write_data(unit_data)

    def _load_w(self, mem, base_addr):
        n = WORD // mem.byte_size

        self._alu.set_input_1(base_addr)
        self._alu.set_op('00')

        word = []

        for i in range(n):
            self._alu.set_input_2(ALU.int_to_n_bit_binary(i))

            addr = self._alu.result

            self._instruction_memory.set_read_address(addr)
            word += list(self._instruction_memory.read_result)

        return word

    def fetch(self):
        instruction = self._load_w(self._instruction_memory, self._pc)

        self._alu.set_input_1(self._pc)
        self._alu.set_input_2(ALU.int_to_n_bit_binary(4))
        self._alu.set_op('00')

        self._pc = self._alu.result

        self._if_id.set_pc(self._pc)
        self._if_id.set_inst(tuple(instruction))

        # end of program
        if instruction == list(ALU.int_to_n_bit_binary(-1)):
            return False
        return True

    def master_control_unit(self, op_code_decimal):
        # memory signals
        self._id_ex_mem_control.Branch = False
        self._id_ex_mem_control.MemRead = False
        self._id_ex_mem_control.MemWrite = False

        # wb signals
        self._id_ex_wb_control.MemToReg = False
        self._id_ex_wb_control.RegWrite = True

        if op_code_decimal == 35:
            self._id_ex_mem_control.MemRead = True
            self._id_ex_wb_control.MemToReg = True
            self._id_ex_wb_control.RegWrite = True
        elif op_code_decimal == 43:
            self._id_ex_mem_control.MemWrite = True
            self._id_ex_wb_control.RegWrite = False
        elif op_code_decimal == 4:
            self._id_ex_mem_control.Branch = False
            self._id_ex_wb_control.RegWrite = False

    def decode(self):

        I_TYPE = [8, 12, 13, 4, 35, 43]

        inst = list(self._if_id.inst)[::-1]
        op_code = inst[31:25:-1]
        op_code_decimal = ALU.n_bit_binary_to_decimal(tuple(op_code))

        # common R type and I type stuff
        if op_code_decimal == 0 or op_code_decimal in I_TYPE:
            rs = inst[25:20:-1]
            rt = inst[20:15:-1]

            # read rt rs
            self._register_file.set_read_r1(tuple(rs))
            self._id_ex.set_rd1(self._register_file.read_d1)

            self._register_file.set_read_r2(tuple(rt))
            self._id_ex.set_rd2(self._register_file.read_d2)

        # if R type
        if op_code_decimal == 0:

            rd = inst[15:10:-1]
            sh = inst[10:5:-1]
            func = inst[5::-1]

            # set registers

            self._id_ex.set_inst_15_11(tuple(rd))

            # ex signals
            self._id_ex_ex_control.ALUOp = tuple(func)
            self._id_ex_ex_control.ALUSource = 'rt'
            self._id_ex_ex_control.RegDst = 'rd'

        # I type
        elif op_code_decimal in I_TYPE:
            imm = inst[15::-1]

            extended_imm = ALU.sign_extend_to(tuple(imm), WORD)
            self._id_ex.set_inst_15_0(extended_imm)

            # ex signals
            self._id_ex_ex_control.ALUOp = ALU.alu_i_type_op_code_table()[op_code_decimal]

            if op_code_decimal == 4:
                s = 'rt'
            else:
                s = 'imm'

            self._id_ex_ex_control.ALUSource = s
            self._id_ex_ex_control.RegDst = 'rt'

        # J
        elif op_code_decimal == 2:
            addr = inst[25::-1]

    def execute(self):
        self._alu.set_op(self._id_ex_ex_control.ALUOp)
        self._alu.set_input_1(self._id_ex.rd1)

        alu_source = self._id_ex_ex_control.ALUSource

        # set the correct alu source
        if alu_source == 'rt':
            input2 = self._id_ex.rd2
        elif alu_source == 'imm':
            input2 = self._id_ex.inst_15_0
        else:
            raise Exception("Invalid ALU source")

        self._alu.set_input_2(input2)
        alu_result = self._alu.result  # *** #
        alu_is_zero = self._alu.zero  # *** #

        # calculate possible beq addr
        self._alu.set_input_1(self._id_ex.pc)
        self._alu.set_input_2(
            ALU.int_to_n_bit_binary(
                ALU.n_bit_binary_to_decimal(
                    self._id_ex.inst_15_0
                ) << 2
            ))

        add_result = self._alu.result  # *** #

        if self._id_ex_ex_control.RegDst == 'rt':
            reg_dest = self._id_ex.rd2  # *** #
        elif self._id_ex_ex_control.RegDst == 'rd':
            reg_des = self._id_ex.inst_15_11

        # propagate wb m control signals
        self._ex_mem_m_control = copy.deepcopy(self._id_ex_mem_control)

        return ALU.n_bit_binary_to_decimal(alu_result)
