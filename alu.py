class ALU:

    @staticmethod
    def validate_n_bit(number):
        """
        Ensures that "number" is a tuple of length more than 0
        :param number:
        :return:
        """

        if type(number) == tuple and len(number) > 0:
            pass
        else:
            raise Exception("Invalid n bit")

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
        if type(number) != tuple and len(number) <= 0:
            raise Exception("Invalid number to sign extend")

        if len(number) > n:
            raise Exception("Exceeded sign extend range")

        if not force_zero:
            sign_bit = number[0]
        else:
            sign_bit = 0

        sign_bits = [sign_bit for i in range(n - len(number))]

        return tuple(sign_bits + list(number))

    @staticmethod
    def int_to_n_bit_binary(i, n):
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
        extended = list(ALU.sign_extend_to(bits, n, force_zero=True))

        if is_negative:
            extended = ALU.twos(tuple(extended))

            # this is overflow
            if extended[0] != 1:
                raise Exception("Overflow")
        else:
            if extended[0] != 0:
                raise Exception("Overflow")

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


