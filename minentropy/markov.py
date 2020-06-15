import math

from mpmath import *

from utils import *

precision = 300


def markov(bits, symbol_length) -> TestResult:
    # logger.debug("MARKOV Test")
    L = len(bits)

    if symbol_length != 1:
        # logger.debug(
        #    "   Warning, Markov test only defined for 1 bit symbols. Setting symbol length to 1",
        # )
        pass

    # # logger.debug(bits)
    # logger.debug("  Symbol Length         1")
    # logger.debug("  Number of bits       ", L)

    # step 1
    count0 = 0
    for bit in bits:
        if bit == 0:
            count0 += 1
    P0 = count0 / L
    P1 = 1.0 - P0

    # Step 2
    C00 = 0
    C01 = 0
    C10 = 0
    C11 = 0

    for i in range(len(bits) - 1):
        if bits[i] == 0 and bits[i + 1] == 0:
            C00 += 1
        if bits[i] == 0 and bits[i + 1] == 1:
            C01 += 1
        if bits[i] == 1 and bits[i + 1] == 0:
            C10 += 1
        if bits[i] == 1 and bits[i + 1] == 1:
            C11 += 1

    P00 = mpf(C00 / (C00 + C01))
    P01 = mpf(C01 / (C00 + C01))
    P10 = mpf(C10 / (C10 + C11))
    P11 = mpf(C11 / (C10 + C11))

    # logger.debug("   ", P00, P01)
    # logger.debug("   ", P10, P11)
    # Step 3

    p_seq = [0.0] * 6
    p_seq[0] = P0 * (P00 ** 127)
    p_seq[1] = P0 * power(P01, 64) * power(P10, 63)
    p_seq[2] = P0 * P01 * (power(P11, 126))
    p_seq[3] = P1 * P10 * (power(P00, 126))
    p_seq[4] = P1 * power(P10, 64) * power(P01, 63)
    p_seq[5] = P1 * power(P11, 127)

    # Step 4

    p_max = max(p_seq)
    min_entropy = -math.log(p_max, 2) / 128.0
    if min_entropy > 1.0:
        min_entropy = 1.0

    # logger.debug("  Min Entropy per bit  ", min_entropy)
    return TestResult(False, None, min_entropy)
