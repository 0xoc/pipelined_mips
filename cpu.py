import copy

from decs import BYTE_SIZE, WORD
from memory import Memory
from alu import ALU
from register_file import RegisterFile
from pipeline_consts import EX_CONTROL, MEM_CONTROL, WB_CONTROL, IF_ID, ID_EX, EX_MEM, MEM_WB, NOOP

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
        self._data_memory = Memory(32, byte_size=BYTE_SIZE)
        self._register_file = RegisterFile(32)
        self._alu = ALU()
        self._pc = ALU.int_to_n_bit_binary(0)

        self._end = False

        # pipe line registers
        self._if_id = IF_ID()
        self._if_id_tmp = IF_ID()

        self._id_ex = ID_EX()
        self._id_ex_tmp = ID_EX()

        self._ex_mem = EX_MEM()
        self._ex_mem_tmp = EX_MEM()

        self._mem_wb = MEM_WB()
        self._mem_wb_tmp = MEM_WB()

    def load_instructions(self, instructions):
        """
        load instructions from an array read from a file
        this is a helper function to initialize the instruction memory
        :param instructions:
        :return:
        """

        memory_cell_size = self._instruction_memory.byte_size

        # times needed to access the memory to fetch one word
        n = 4

        # start putting instruction into memory from address 0
        base_addr = ALU.int_to_n_bit_binary(0)

        self._instruction_memory.set_mem_write(True)

        for j in range(len(instructions)):
            instruction = instructions[j]
            inst = [int(c) for c in instruction.replace('\n', '').replace(' ', '').split(';')[0]]

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

        self._instruction_memory.set_mem_write(False)

    def _load_w(self, mem, base_addr, memRead=True):

        if not memRead:
            return ALU.int_to_n_bit_binary(0)

        n = 4
        self._alu.set_input_1(base_addr)
        self._alu.set_op('00')

        word = []

        for i in range(n):
            self._alu.set_input_2(ALU.int_to_n_bit_binary(i))
            addr = self._alu.result
            word += list(mem.at(addr))

        return word

    def _store_w(self, base_addr, word, memWrite=True):

        if not memWrite:
            return
        self._alu.set_input_1(base_addr)
        self._alu.set_op('00')

        for i in range(4):
            self._alu.set_input_2(ALU.int_to_n_bit_binary(i))
            addr = self._alu.result

            byte = tuple(word[i * 8: 8 * (i + 1)])
            self._data_memory.put(addr, byte)

    def cycle(self):
        # pipe line register
        self._if_id = copy.deepcopy(self._if_id_tmp)
        self._id_ex = copy.deepcopy(self._id_ex_tmp)
        self._ex_mem = copy.deepcopy(self._ex_mem_tmp)
        self._mem_wb = copy.deepcopy(self._mem_wb_tmp)

        self.fetch()
        self.decode()
        self.execute()
        self.memory()
        self.write_back()

    def master_control_unit(self, op_code_decimal, stall=False):

        if stall:
            # memory signals

            self._id_ex_tmp.mem_control.MemRead = False
            self._id_ex_tmp.mem_control.MemWrite = False
            self._id_ex_tmp.wb_control.RegWrite = False

            return

        # memory signals
        self._id_ex_tmp.mem_control.Branch = False
        self._id_ex_tmp.mem_control.MemRead = False
        self._id_ex_tmp.mem_control.MemWrite = False

        # wb signals
        self._id_ex_tmp.wb_control.MemToReg = False
        self._id_ex_tmp.wb_control.RegWrite = True

        if op_code_decimal == 35:
            self._id_ex_tmp.mem_control.MemRead = True
            self._id_ex_tmp.wb_control.MemToReg = True

        elif op_code_decimal == 43:
            self._id_ex_tmp.mem_control.MemWrite = True
            self._id_ex_tmp.wb_control.RegWrite = False

        elif op_code_decimal == 4:
            self._id_ex_tmp.mem_control.Branch = True
            self._id_ex_tmp.wb_control.RegWrite = False

    def forwarding_unit(self):

        result = {
            'ForwardA': '00',
            'ForwardB': '00',
        }

        # EX Hazard
        if (self._ex_mem.wb_control.RegWrite
                and (self._ex_mem.reg_dest != ALU.int_to_n_bit_binary(0, 5))
                and (self._ex_mem.reg_dest == self._id_ex.rs)):
            result['ForwardA'] = '10'

        if (self._ex_mem.wb_control.RegWrite
                and (self._ex_mem.reg_dest != ALU.int_to_n_bit_binary(0, 5))
                and (self._ex_mem.reg_dest == self._id_ex.rt)):
            result['ForwardB'] = '10'

        # memory hazard
        if (
                self._mem_wb.wb_control.RegWrite
                and self._mem_wb.reg_dest != ALU.int_to_n_bit_binary(0, 5)
                and not (
                self._ex_mem.wb_control.RegWrite and (self._ex_mem.reg_dest != ALU.int_to_n_bit_binary(0, 5))
                and (self._ex_mem.reg_dest == self._id_ex.rs)
        )
                and (self._mem_wb.reg_dest == self._id_ex.rs)):
            result['ForwardA'] = '01'

        if (self._mem_wb.wb_control.RegWrite
                and (self._mem_wb.reg_dest != ALU.int_to_n_bit_binary(0, 5))
                and not (self._ex_mem.wb_control.RegWrite and (self._ex_mem.reg_dest != ALU.int_to_n_bit_binary(0, 5))
                         and (self._ex_mem.reg_dest == self._id_ex.rt))
                and (self._mem_wb.reg_dest == self._id_ex.rt)):
            result['ForwardB'] = '01'

        return result

    def fetch(self):
        instruction = self._load_w(self._instruction_memory, self._pc)
        self._pc = ALU.n_bit_binary_to_decimal(self._pc) + 4
        self._pc = ALU.int_to_n_bit_binary(self._pc)

        # end of program
        if instruction == list(ALU.int_to_n_bit_binary(-1)):
            self._end = True

        if self._end:
            instruction = NOOP
            self._if_id_tmp.set_inst(tuple(instruction))
        else:
            self._if_id_tmp.set_pc(self._pc)
            self._if_id_tmp.set_inst(tuple(instruction))

    def decode(self):
        pipeline_register = self._if_id

        I_TYPE = [8, 12, 13, 4, 35, 43]

        if list(pipeline_register.inst) == NOOP:
            self.master_control_unit(op_code_decimal=0, stall=True)
            return

        inst = list(pipeline_register.inst)[::-1]
        rs = inst[25:20:-1]
        rt = inst[20:15:-1]

        # hazard detection
        if self._id_ex.mem_control.MemRead and (self._id_ex.rt == tuple(rs) or self._id_ex.rt == tuple(rt)):
            self._pc = ALU.int_to_n_bit_binary(
                ALU.n_bit_binary_to_decimal(self._pc) - 4,
            )

            self._if_id_tmp.set_inst(tuple(inst[::-1]))
            self._if_id_tmp.set_pc(self._pc)
            self.master_control_unit(op_code_decimal=0, stall=True)

            return

        op_code = inst[31:25:-1]
        op_code_decimal = ALU.n_bit_binary_to_decimal(tuple(op_code), signed=False)

        self.master_control_unit(op_code_decimal)

        # common R type and I type stuff
        if op_code_decimal == 0 or op_code_decimal in I_TYPE:
            # read rt rs

            self._id_ex_tmp.set_rd1(self._register_file.at(tuple(rs)))
            self._id_ex_tmp.set_rd2(self._register_file.at(tuple(rt)))

            self._id_ex_tmp.set_rs(tuple(rs))
            self._id_ex_tmp.set_rt(tuple(rt))

        # if R type
        if op_code_decimal == 0:
            rd = inst[15:10:-1]
            func = inst[5::-1]

            # set registers

            self._id_ex_tmp.set_inst_rd(tuple(rd))

            # ex signals
            self._id_ex_tmp.ex_control.ALUOp = tuple(func)

            self._id_ex_tmp.ex_control.ALUSource = 'rt'
            self._id_ex_tmp.ex_control.RegDst = 'rd'

        # I type
        elif op_code_decimal in I_TYPE:
            imm = inst[15::-1]

            extended_imm = ALU.sign_extend_to(tuple(imm), WORD)
            self._id_ex_tmp.set_inst_imm(extended_imm)

            # ex signals
            self._id_ex_tmp.ex_control.ALUOp = ALU.alu_i_type_op_code_table()[op_code_decimal]

            if op_code_decimal == 4:
                s = 'rt'
            else:
                s = 'imm'

            self._id_ex_tmp.ex_control.ALUSource = s
            self._id_ex_tmp.ex_control.RegDst = 'rt'

        # J
        elif op_code_decimal == 2:
            addr = inst[25::-1]

        self._id_ex_tmp.set_pc(pipeline_register.pc)

    def execute(self):

        pipeline_register = copy.deepcopy(self._id_ex)

        self._alu.set_op(pipeline_register.ex_control.ALUOp)

        fu_data = self.forwarding_unit()

        if fu_data['ForwardA'] == '00':
            input1 = pipeline_register.rd1
        elif fu_data['ForwardA'] == '10':
            input1 = self._ex_mem.alu_result
        elif fu_data['ForwardA'] == '01':
            input1 = self.write_back(ex=False)
        else:
            raise Exception("Invalid input 1 ")

        self._alu.set_input_1(input1)

        alu_source = pipeline_register.ex_control.ALUSource

        # memory data forward
        if fu_data['ForwardB'] == '00':
            memory_data = pipeline_register.rd2
        elif fu_data['ForwardB'] == '10':
            memory_data = self._ex_mem.alu_result
        elif fu_data['ForwardB'] == '01':
            memory_data = self.write_back(ex=False)
        else:
            Exception("Error")

        # set the correct alu source
        if alu_source == 'imm':
            input2 = pipeline_register.inst_imm

        elif fu_data['ForwardB'] == '00':
            if alu_source == 'rt':
                input2 = pipeline_register.rd2
            elif alu_source == 'rs':
                input2 = pipeline_register.rd1
        elif fu_data['ForwardB'] == '10':
            input2 = self._ex_mem.alu_result
        elif fu_data['ForwardB'] == '01':
            input2 = self.write_back(ex=False)
        else:
            raise Exception("Invalid ALU source")

        self._alu.set_input_2(input2)
        alu_result = self._alu.result
        alu_is_zero = self._alu.zero

        # calculate possible beq addr
        pc = ALU.n_bit_binary_to_decimal(pipeline_register.pc)
        offset_4 = ALU.n_bit_binary_to_decimal(
            pipeline_register.inst_imm
        ) * 4

        jump_target = ALU.int_to_n_bit_binary(pc + offset_4)

        if pipeline_register.mem_control.Branch and alu_is_zero:
            self._pc = jump_target

        if pipeline_register.ex_control.RegDst == 'rt':
            reg_dest = pipeline_register.rt
        elif pipeline_register.ex_control.RegDst == 'rd':
            reg_dest = pipeline_register.inst_rd

        # propagate wb m control signals
        self._ex_mem_tmp.mem_control = copy.deepcopy(pipeline_register.mem_control)
        self._ex_mem_tmp.wb_control = copy.deepcopy(pipeline_register.wb_control)

        self._ex_mem_tmp.set_alu_result(alu_result)
        self._ex_mem_tmp.set_alu_zero_flag(alu_is_zero)
        self._ex_mem_tmp.set_jump_target(jump_target)
        self._ex_mem_tmp.set_rd2(memory_data)
        self._ex_mem_tmp.set_reg_dest(reg_dest)

        self._ex_mem_tmp.pc = pipeline_register.pc

    def memory(self):
        pipeline_data = copy.deepcopy(self._ex_mem)

        if pipeline_data.mem_control.MemWrite:
            self._store_w(pipeline_data.alu_result, pipeline_data.rd2, pipeline_data.mem_control.MemWrite)

        if pipeline_data.mem_control.MemRead:
            read_result = self._load_w(self._data_memory, pipeline_data.alu_result, pipeline_data.mem_control.MemRead)
            self._mem_wb_tmp.set_read_data(tuple(read_result))

        self._mem_wb_tmp.set_alu_result(pipeline_data.alu_result)
        self._mem_wb_tmp.set_reg_dest(pipeline_data.reg_dest)
        self._mem_wb_tmp.wb_control = copy.deepcopy(pipeline_data.wb_control)
        self._mem_wb_tmp.pc = pipeline_data.pc

    def write_back(self, ex=True):
        pipeline_data = self._mem_wb

        if pipeline_data.wb_control.MemToReg:
            write_data = pipeline_data.read_data
        else:
            write_data = pipeline_data.alu_result

        # to be forwarded
        if not ex:
            return write_data

        # set register signals

        if pipeline_data.wb_control.RegWrite:
            if pipeline_data.reg_dest == (0, 0, 0, 1, 0):
                print("the: ", ALU.n_bit_binary_to_decimal(pipeline_data.pc))
            self._register_file.put(pipeline_data.reg_dest, write_data)
