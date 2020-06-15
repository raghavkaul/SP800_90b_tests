from qcore.asserts import assert_eq
from qcore.testing import disabled


@disabled
def test_ttuple():
    from ttuple import ttuple

    symbols = [2, 2, 0, 1, 0, 2, 0, 1, 2, 1, 2, 0, 1, 2, 1, 0, 0, 1, 0, 0, 0]
    bits = [format(s, "2b") for s in symbols]
    (iid_assumption, T, min_entropy) = ttuple(
        bits, symbol_length=2, threshold=3
    )

    print("min_entropy = ", min_entropy)


@disabled
def test_multi_mmc_prediction():
    symbols = [2, 1, 3, 2, 1, 3, 1, 3, 1]
    bits = [format(s, "2b") for s in symbols]
    (iid_assumption, T, min_entropy) = multi_mmc_prediction(
        bits, verbose=True, symbol_length=2, D=3
    )

    print("min_entropy = ", min_entropy)


@disabled
def test_multi_mcw():
    symbols = [1, 2, 1, 0, 2, 1, 1, 2, 2, 0, 0, 0]
    bits = [format(s, "2b") for s in symbols]
    (iid_assumption, T, min_entropy) = multi_mcw(
        bits, symbol_length=2, ws=[0, 3, 5, 7, 9]
    )

    print("min_entropy = ", min_entropy)


def test_mcv():
    data = [0, 1, 1, 2, 0, 1, 2, 2, 0, 1, 0, 1, 1, 0, 2, 2, 1, 0, 2, 1]

    from mcv import mcv

    assert_eq(0.5363, mcv(data).min_entropy, tolerance=0.0001)


@disabled
def test_markov():
    # fmt: off
    bits = [
        1,
        0,
        0,
        0,
        1,
        1,
        1,
        0,
        0,
        1,
        0,
        1,
        0,
        1,
        0,
        1,
        1,
        1,
        0,
        0,
        1,
        1,
        0,
        0,
        0,
        1,
        1,
        1,
        0,
        0,
        1,
        0,
        1,
        0,
        1,
        0,
        1,
        1,
        1,
        0,
    ]
    # fmt: on
    (iid_assumption, T, min_entropy) = markov(bits, 1)

    print("min_entropy = ", min_entropy)


@disabled
def test_lz78y():
    symbols = [2, 1, 3, 2, 1, 3, 1, 3, 1, 2, 1, 3, 2]
    bits = [format(s, "2b") for s in symbols]
    (iid_assumption, T, min_entropy) = lz78y(bits, symbol_length=2, B=4)

    print("min_entropy = ", min_entropy)


@disabled
def test_lrs():
    symbols = [2, 2, 0, 1, 0, 2, 0, 1, 2, 1, 2, 0, 1, 2, 1, 0, 0, 1, 0, 0, 0]
    bits = [format(s, "2b") for s in symbols]
    (iid_assumption, T, min_entropy) = lrs(
        bits, symbol_length=2, verbose=True, threshold=3
    )

    print("min_entropy = ", min_entropy)


@disabled
def test_lag_prediction():
    symbols = [2, 1, 3, 2, 1, 3, 1, 3, 1, 2]
    bits = [format(s, "2b") for s in symbols]
    (iid_assumption, T, min_entropy) = lag_prediction(
        bits, symbol_length=2, D=3
    )

    print("min_entropy = ", min_entropy)


@disabled
def test_compression():
    import compression

    # fmt: off
    bits = [1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1]
    # fmt: on
    (iid_assumption, T, min_entropy) = compression.compression(bits, 1, d=4)

    print("min_entropy = ", min_entropy)


def test_collision():
    # fmt: off
    data = [1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0]
    # fmt: on

    import collision

    assert_eq(0.4483, collision.collision(data).min_entropy, tolerance=0.0001)
