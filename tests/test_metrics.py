from qcore.asserts import assert_eq


def test_ttuple():
    # NB: This test seems to handle strings as well.
    symbols = [2, 2, 0, 1, 0, 2, 0, 1, 2, 1, 2, 0, 1, 2, 1, 0, 0, 1, 0, 0, 0]

    import ttuple

    assert_eq(
        0.273, ttuple.ttuple(symbols, threshold=3).min_entropy, tolerance=0.001,
    )


def test_multi_mmc_prediction():
    symbols = [2, 1, 3, 2, 1, 3, 1, 3, 1]

    import multi_mmc_prediction

    assert_eq(
        0.0755,
        multi_mmc_prediction.multi_mmc_prediction(symbols, D=3).min_entropy,
        tolerance=0.0001,
    )


def test_multi_mcw():
    # NB: This test also works on strings
    symbols = [1, 2, 1, 0, 2, 1, 1, 2, 2, 0, 0, 0]
    import multi_mcw

    assert_eq(
        0.3908,
        multi_mcw.multi_mcw(symbols, ws=[0, 3, 5, 7, 9]).min_entropy,
        tolerance=0.0001,
    )


def test_mcv():
    data = [0, 1, 1, 2, 0, 1, 2, 2, 0, 1, 0, 1, 1, 0, 2, 2, 1, 0, 2, 1]

    from mcv import mcv

    assert_eq(0.5363, mcv(data).min_entropy, tolerance=0.0001)


def test_markov():
    # fmt: off
    bits = [1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0]
    # fmt: on

    import markov

    assert_eq(
        0.761, markov.markov(bits).min_entropy, tolerance=0.001,
    )


def test_lz78y():
    symbols = [2, 1, 3, 2, 1, 3, 1, 3, 1, 2, 1, 3, 2]

    import lz78y

    assert_eq(0.0191, lz78y.lz78y(symbols, B=4).min_entropy, tolerance=0.0001)


def test_lrs():
    # NB: This test handles strings
    symbols = [2, 2, 0, 1, 0, 2, 0, 1, 2, 1, 2, 0, 1, 2, 1, 0, 0, 1, 0, 0, 0]

    import lrs

    assert_eq(
        0.6146, lrs.lrs(symbols, threshold=3).min_entropy, tolerance=0.0001
    )


def test_lag_prediction():
    # NB: This test handles strings
    symbols = [2, 1, 3, 2, 1, 3, 1, 3, 1, 2]

    import lag_prediction

    assert_eq(
        0.735,
        lag_prediction.lag_prediction(symbols, D=3).min_entropy,
        tolerance=0.001,
    )


def test_compression():
    # fmt: off
    bits = [1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 1, 0, 0, 0, 1, 1]
    # fmt: on
    bits = "".join(map(str, bits))

    import compression

    assert_eq(
        0.1345, compression.compression(bits, d=4).min_entropy, tolerance=0.0001
    )


def test_collision():
    # fmt: off
    data = [1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 0]
    # fmt: on

    import collision

    assert_eq(0.4483, collision.collision(data).min_entropy, tolerance=0.0001)
