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

        # read registers
        self._read_r1 = ALU.int_to_n_bit_binary(0, 5)
        self._read_r2 = ALU.int_to_n_bit_binary(0, 5)

        # register read data
        self.read_d1 = ALU.int_to_n_bit_binary(0)
        self.read_d2 = ALU.int_to_n_bit_binary(0)

        # write enable and write register write data
        self.reg_write = False
        self._write_r = ALU.int_to_n_bit_binary(0, 5)
        self._write_data = ALU.int_to_n_bit_binary(0)

    def _exc(self):
        self.read_data_x('1')
        self.read_data_x('2')
        self.write()

    def validate_register(self, register):
        """

        :param register: validate the given register by type, length, and existence
        :return:
        """
        if not (type(register) == tuple and
                len(register) == self.register_size and
                register in self.data.keys()):
            raise Exception("Invalid register")

    def validate_data(self, data):
        """
        :param data: validate by type and length
        :return:
        """
        if not (type(data) == tuple and len(data) == self.register_size):
            raise Exception("Invalid register data")

    def at(self, register):
        """

        :param register:
        :return: content of the given register
        """
        self.validate_register(register)
        return self.data[register]

    def put(self, register, data):
        """

        :param register:
        :param data:
        :return:
        """

        self.validate_register(register)
        self.validate_data(data)

        self.data[register] = data

    def set_read_r1(self, register):
        self.validate_register(register)
        self._read_r1 = register

        self._exc()

    def set_read_r2(self, register):
        self.validate_register(register)
        self._read_r2 = register

        self._exc()

    def set_write_r(self, register):
        self.validate_data(register)
        self._write_r = register

        self._exc()

    def set_write_data(self, data):
        self.validate_data(data)
        self._write_data = data

        self._exc()

    def read_data_x(self, x):
        """
        set read_x by content at read_x
        :return: data at read_x
        """

        read_addr = self._read_r1 if x == 1 else self._read_r2

        data = self.at(read_addr)

        if x == 1:
            self.read_d1 = data
        else:
            self.read_d2 = data

        return data

    def write(self):
        if self.reg_write:
            self.put(self._write_r, self._write_data)
