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
            assert rg.read_d1 == ALU.int_to_n_bit_binary(i)
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


def mem_test():

    def mem_result_decimal(mem):
        return ALU.n_bit_binary_to_decimal(mem.read_result)

    mem = Memory(10)

    mem.set_write_addr(ALU.int_to_n_bit_binary(0))
    mem.set_write_data(ALU.int_to_n_bit_binary(5))

    mem.set_mem_read(True)
    mem.set_read_address(ALU.int_to_n_bit_binary(0))

    assert mem_result_decimal(mem) == 0
    mem.set_mem_read(False)
    mem.set_mem_write(True)
    assert mem_result_decimal(mem) == 0
    mem.set_mem_read(True)
    assert mem_result_decimal(mem) == 5


tests = [register_file_test, alu_test, mem_test]

for test in tests:
    test()
    print("%s passed" % test.__name__)

