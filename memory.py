from alu import ALU
from decs import BYTE_SIZE, WORD


class Memory:

    def __init__(self, n, byte_size=WORD, addr_size=WORD):
        """
        :param
            n: size of memory in bytes
        """
        self.data = {}
        self.size = n
        self.byte_size = byte_size
        self.addr_size = addr_size

        # initialize an array of memory with addresses starting from 0 to n - 1
        for i in range(n):
            self.data[ALU.int_to_n_bit_binary(i, addr_size)] = ALU.int_to_n_bit_binary(0, byte_size)

        # read write addresses
        self._read_address = ALU.int_to_n_bit_binary(0, addr_size)
        self._write_address = ALU.int_to_n_bit_binary(0, addr_size)

        self.read_result = ALU.int_to_n_bit_binary(0, byte_size)
        self._write_data = ALU.int_to_n_bit_binary(0, byte_size)

        self._mem_read = False
        self._mem_write = False

    def _exc(self):
        """
        runs at every clock
        :return:
        """

        self.write()
        self.read()

    def validate_addr(self, addr):
        """
        validate addr by type, length and existence
        :param addr:
        :return:
        """

        if not (type(addr) == tuple and
                len(addr) == self.addr_size and
                addr in self.data.keys()
        ):
            raise Exception("Invalid addr")

    def validate_byte(self, byte):
        """
        validate by type and length
        :param byte:
        :return:
        """
        if not (type(byte) == tuple and len(byte) == self.byte_size):
            raise Exception("Invalid byte")

    def at(self, addr):
        """
        :param addr: 32 bit add tuple
        :return: one byte binary data in the given addr
        """

        self.validate_addr(addr)

        return self.data[addr]

    def put(self, addr, byte):
        """

        :param addr: addr to write the byte to
        :param byte: byte to be writen
        :return: the written byte
        """
        self.validate_addr(addr)
        self.validate_byte(byte)

        self.data[addr] = byte

        return byte

    def set_read_address(self, addr):
        self.validate_addr(addr)
        self._read_address = addr

        self._exc()

    def set_write_addr(self, addr):
        self.validate_addr(addr)
        self._write_address = addr

        self._exc()

    def set_write_data(self, data):
        self.validate_byte(data)
        self._write_data = data

        self._exc()

    def set_mem_read(self, mem_read):
        self._mem_read = mem_read

        self._exc()

    def set_mem_write(self, mem_write):
        self._mem_write = mem_write

        self._exc()

    def read(self):
        """
        return memory content at read_address if mem_read is True
        :return:
        """
        if self._mem_read:
            self.read_result = self.at(self._read_address)
            return self.read_result

    def write(self):
        """
        write write_data = write address if mem_write is True
        :return:
        """

        if self._mem_write:
            self.put(self._write_address, self._write_data)