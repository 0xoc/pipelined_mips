from alu import ALU


class Memory:

    def __init__(self, n):
        """
        :param
            n: size of memory in bytes
        """
        self.data = {}
        self.size = n

        # initialize an array of memory with addresses starting from 0 to n - 1
        for i in range(n):
            self.data[ALU.int_to_n_bit_binary(i, 32)] = ALU.int_to_n_bit_binary(0, 8)

    def validate_addr(self, addr):
        if type(addr) == tuple and len(addr) == 32:
            pass
        elif addr in self.data.keys():
            pass
        else:
            raise Exception("Invalid addr")

    @staticmethod
    def validate_byte(byte):
        if type(byte) == tuple and len(byte) == 8:
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
