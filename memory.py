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
            self.data[ALU.int_to_n_bit_binary(32, addr_size)] = ALU.int_to_n_bit_binary(byte_size)

        # read write addresses
        self.read_address = ALU.int_to_n_bit_binary(0, addr_size)
        self.write_address = ALU.int_to_n_bit_binary(0, addr_size)

        self.write_data = ALU.int_to_n_bit_binary(0, byte_size)

        self.mem_read = False
        self.mem_write = False

    def validate_addr(self, addr):
        if type(addr) == tuple and len(addr) == self.addr_size:
            pass
        elif addr in self.data.keys():
            pass
        else:
            raise Exception("Invalid addr")

    def validate_byte(self, byte):
        if type(byte) == tuple and len(byte) == self.byte_size:
            pass
        else:
            raise Exception("Invalid byte")

    def at(self, addr):
        """
        :param addr: 32 bit add tuple
        :return: one byte binary data in the given addr
        """

        self.validate_addr(addr)

        return self.data[addr]

    def read(self):
        """
        return memory content at read_address if mem_read is True
        :return:
        """
        if self.mem_read:
            return self.at(self.read_address)

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

    def write(self):
        """
        write write_data = write address if mem_write is True
        :return:
        """

        if self.mem_write:
            self.put(self.write_address, self.write_data)
