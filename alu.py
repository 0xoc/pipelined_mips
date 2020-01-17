class ALU:

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

        if len(bits) > n:
            raise Exception("Exceeded number of bits requested")

        bits.reverse()
        extended = list(ALU.sign_extend_to(bits, n, force_zero=True))

        if is_negative:
            first_one_seen = False
            for i in range(len(extended) - 1, -1, -1):
                if extended[i] == 1 and not first_one_seen:
                    first_one_seen = True
                elif first_one_seen:
                    extended[i] = extended[i] ^ 1

            # this is overflow
            if extended[0] != 1:
                raise Exception("Overflow")

        else:
            if extended[0] != 0:
                raise Exception("Overflow")

        return tuple(extended)

