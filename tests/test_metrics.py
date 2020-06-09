def test_ttuple():
    bits = list()
    symbols = [2, 2, 0, 1, 0, 2, 0, 1, 2, 1, 2, 0, 1, 2, 1, 0, 0, 1, 0, 0, 0]
    for s in symbols:
        bits = bits + int_to_bits(s, 2)
    (iid_assumption, T, min_entropy) = ttuple(bits, symbol_length=2, threshold=3)

    logger.debug("min_entropy = ", min_entropy)


def test_multi_mmc_prediction():
    bits = list()
    symbols = [2, 1, 3, 2, 1, 3, 1, 3, 1]

    for s in symbols:
        bits = bits + int_to_bits(s, 2)
    (iid_assumption, T, min_entropy) = multi_mmc_prediction(
        bits, verbose=True, symbol_length=2, D=3
    )

    print("min_entropy = ", min_entropy)


def test_multi_mcw():
    bits = list()
    symbols = [1, 2, 1, 0, 2, 1, 1, 2, 2, 0, 0, 0]
    for s in symbols:
        bits = bits + int_to_bits(s, 2)
    (iid_assumption, T, min_entropy) = multi_mcw(
        bits, symbol_length=2, ws=[0, 3, 5, 7, 9]
    )

    logger.debug("min_entropy = ", min_entropy)


def test_mcv():
    bits = [
        0,
        0,
        0,
        1,
        0,
        1,
        1,
        0,
        0,
        0,
        0,
        1,
        1,
        0,
        1,
        0,
        0,
        0,
        0,
        1,
        0,
        0,
        0,
        1,
        0,
        1,
        0,
        0,
        1,
        0,
        1,
        0,
        0,
        1,
        0,
        0,
        1,
        0,
        0,
        1,
    ]
    (iid_assumption, T, min_entropy) = mcv(bits, 2)

    logger.debug("min_entropy = ", min_entropy)


def test_markov():
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
    (iid_assumption, T, min_entropy) = markov(bits, 1)

    logger.debug("min_entropy = ", min_entropy)


def test_lz78y():
    bits = list()
    symbols = [2, 1, 3, 2, 1, 3, 1, 3, 1, 2, 1, 3, 2]

    for s in symbols:
        bits = bits + int_to_bits(s, 2)
    (iid_assumption, T, min_entropy) = lz78y(bits, symbol_length=2, B=4)

    logger.debug("min_entropy = ", min_entropy)


def test_lrs():
    bits = list()
    symbols = [2, 2, 0, 1, 0, 2, 0, 1, 2, 1, 2, 0, 1, 2, 1, 0, 0, 1, 0, 0, 0]
    for s in symbols:
        bits = bits + int_to_bits(s, 2)
    (iid_assumption, T, min_entropy) = lrs(
        bits, symbol_length=2, verbose=True, threshold=3
    )

    logger.debug("min_entropy = ", min_entropy)


def test_lag_prediction():
    bits = list()
    symbols = [2, 1, 3, 2, 1, 3, 1, 3, 1, 2]
    for s in symbols:
        bits = bits + int_to_bits(s, 2)
    (iid_assumption, T, min_entropy) = lag_prediction(bits, symbol_length=2, D=3)

    logger.debug("min_entropy = ", min_entropy)


def test_compression():
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
        1,
        1,
        1,
        0,
        0,
        0,
        1,
        1,
    ]

    (iid_assumption, T, min_entropy) = compression(bits, 1, d=4)

    logger.debug("min_entropy = ", min_entropy)


def test_collision():
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

    (iid_assumption, T, min_entropy) = collision(bits, 1)

    logger.debug("min_entropy = ", min_entropy)
