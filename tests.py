from memory import Memory
from alu import ALU
from register_file import RegisterFile
from decs import BYTE_SIZE, WORD


def register_file_test():
    rg = RegisterFile()

    rg.reg_write = True

    i = 0
    for k in rg.data.keys():

        if i >= 10:
            rg.reg_write = False

        rg.set_read_r1(k)
        rg.set_read_r2(k)

        old_d1 = rg.read_d1
        old_d2 = rg.read_d2

        rg.set_write_r(k)
        rg.set_write_data(ALU.int_to_n_bit_binary(i))

        assert rg.read_d1 == rg.read_d2

        if i < 10:
            try:
                assert rg.read_d1 == ALU.int_to_n_bit_binary(i)
            except:
                print(i, rg.read_d1, ALU.int_to_n_bit_binary(i))
        else:
            assert rg.read_d1 == old_d1

        i += 1


def alu_test():

    def get_decimal_result(alu):
        r = alu.result
        d = alu.n_bit_binary_to_decimal(r)

        return d

    alu = ALU()
    alu.set_input_1(alu.int_to_n_bit_binary(20))
    alu.set_input_2(alu.int_to_n_bit_binary(12))

    assert get_decimal_result(alu) == 32
    alu.set_op('01')
    assert get_decimal_result(alu) == 240
    alu.set_op('11')
    assert get_decimal_result(alu) == 8


tests = []
tests += [register_file_test, alu_test]

for test in tests:
    test()
