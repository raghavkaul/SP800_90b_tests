from qcore.asserts import assert_eq

import encoders


def test_bitwise_resize():
    assert_eq(
        # fmt: off
        [1, 1, 1,
         1, 0, 1,
         0, 0, 1,
         0, 1, 0,
         0, 0, 0],
        # fmt: on
        encoders.bitwise_resize(
            [0b111, 0b101, 0b001, 0b010, 0b000], new_bitwidth=1
        ),
    )


def test_encode_distinct():
    assert_eq([0, 1, 2, 0], encoders.encode_distinct(["a", "b", "c", "a"]))
