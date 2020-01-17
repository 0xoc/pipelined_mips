from decs import BYTE_SIZE, WORD


class ALU:

    def __init__(self, input_size=WORD, output_size=WORD):
        self.input_size = input_size
        self.output_size = output_size

        self.result = 0
        self.zero = True

        self.op_table = {
            '00': lambda a, b: a + b,
            '01': lambda a, b: a * b,
            '11': lambda a, b: a - b
        }

    @staticmethod
    def validate_n_bit(number):
        """
        Ensures that "number" is a tuple of length more than 0
        :param number:
        :return:
        """

        if not (type(number) == tuple and len(number) > 0):
            raise Exception("Invalid n bit")

    def validate_input(self, i):
        """

        :param i: input to be validated, tuple and input_size bits
        :return:
        """

        if not (type(i) == tuple and len(i) == self.input_size):
            raise Exception("Invalid Input")

    @staticmethod
    def twos(number):
        """

        :param number:
        :return: two's complement of the number
        """
        ALU.validate_n_bit(number)

        number = list(number)
        seen_first_one = False
        for i in range(len(number) - 1, -1, -1):
            if number[i] == 1 and not seen_first_one:
                seen_first_one = True
            elif seen_first_one:
                number[i] = number[i] ^ 1
        return tuple(number)

    @staticmethod
    def sign_extend_to(number, n, force_zero=False):
        """

        :param number: number to be sign extended
        :param n: total length after sign extension
        :param force_zero: if set sign bit will be set to 0
        :return: sign extended number
        """
        ALU.validate_n_bit(number)

        if len(number) > n:
            raise Exception("Exceeded sign extend range")

        if not force_zero:
            sign_bit = number[0]
        else:
            sign_bit = 0

        sign_bits = [sign_bit for i in range(n - len(number))]

        return tuple(sign_bits + list(number))

    @staticmethod
    def int_to_n_bit_binary(i, n=WORD):
        """
        :param
            i: integer to be converted to a tuple of n bits
            n: number of bits to represent i in
        :return: a tuple of n bits representing i in binary
        """

        if i == 0:
            return tuple([0 for c in range(n)])

        # if i is negative, make it positive and
        # set a flag to compute 2's complement at the end
        elif i < 0:
            is_negative = True
            i *= -1
        else:
            is_negative = False

        bits = []

        while i > 0:
            r = i % 2
            i = i // 2
            bits += [r]

        bits.reverse()
        extended = list(ALU.sign_extend_to(tuple(bits), n, force_zero=True))

        if is_negative:
            extended = ALU.twos(tuple(extended))

        return tuple(extended)

    @staticmethod
    def n_bit_binary_to_decimal(number):
        ALU.validate_n_bit(number)

        is_negative = False
        # if number is negative
        if number[0] == 1:
            number = ALU.twos(number)
            is_negative = True

        decimal = 0
        for i in number:
            decimal = decimal * 2 + i

        if is_negative:
            return -decimal
        return decimal

    def exc(self, input1, input2, op):
        self.validate_input(input1)
        self.validate_input(input2)

        input1_decimal = self.n_bit_binary_to_decimal(input1)
        input2_decimal = self.n_bit_binary_to_decimal(input2)

        result_decimal = self.op_table[op](input1_decimal, input2_decimal)

        if result_decimal == 0:
            self.result = self.int_to_n_bit_binary(0, self.output_size)
            self.zero = True

        self.result = self.int_to_n_bit_binary(result_decimal, self.output_size)
        self.zero = False

        return self.result
