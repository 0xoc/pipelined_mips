from decs import BYTE_SIZE, WORD
from memory import Memory
from alu import ALU
from register_file import RegisterFile
from pipeline_consts import EX_CONTROL, MEM_CONTROL, WB_CONTROL, IF_ID

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
        self._register_file = RegisterFile(1024)
        self._alu = ALU()
        self._pc = ALU.int_to_n_bit_binary(0)

        # pipe line registers
        self._if_id = RegisterFile(count=2)
        self._id_ex = RegisterFile(count=6)
        self._ex_mem = RegisterFile(count=5)
        self._mem_wb = RegisterFile(count=3)

        # pipe line controls
        self._ex_control = EX_CONTROL()
        self._mem_control = MEM_CONTROL()
        self._wb_control = WB_CONTROL()

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

    @staticmethod
    def _bulk_register_set(register_file, data_dict):
        register_file.set_register_write(True)

        for reg in data_dict.keys():
            register_file.set_write_r(reg)
            register_file.set_write_data(data_dict[reg])

    def fetch(self):
        instruction = self._load_w(self._instruction_memory, self._pc)

        self._alu.set_input_1(self._pc)
        self._alu.set_input_2(ALU.int_to_n_bit_binary(4))
        self._alu.set_op('00')

        self._pc = self._alu.result

        self._bulk_register_set(self._if_id, {
            IF_ID.PC: self._pc,
            IF_ID.INST: tuple(instruction)
        })

        self._if_id.set_read_r1(IF_ID.INST)

    def decode(self):
        pass