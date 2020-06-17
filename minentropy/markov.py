import numpy as np
from mpmath import *

from utils import *
from encoders import bitwise_resize

# We are about to exponentiate some big numbers
power_bigint = lambda base, exponent: power(mpf(base), exponent)


def markov(data: DataSequence) -> TestResult:
    # TODO: Documentation
    data = bitwise_resize(data, new_bitwidth=1)
    L = len(data)

    # Step 1: Get bitwise probabilities
    counts = np.unique(data, return_counts=True)[1]
    P0, P1 = counts / L

    # Step 2: Create a bitwise transition matrix
    # C[i][j] represents the count of transitions from i->j in a bitstream
    C = np.zeros((2, 2))

    # NB: Only recording non-overlapping transitions. E.g.:
    # 0101 -> recorded as N=2 {0->1, 0->1}, not N=3 {0->1, 1->0, 0->1}
    for i in range(len(data) - 1):
        C[data[i]][data[i + 1]] += 1

    # P[i][j] represents the probability of a transition to j, given i, in a bitstream
    P00 = C[0][0] / (C[0][0] + C[0][1])
    P01 = C[0][1] / (C[0][0] + C[0][1])
    P10 = C[1][0] / (C[1][0] + C[1][1])
    P11 = C[1][1] / (C[1][0] + C[1][1])

    # Step 3: Find probabilities of most likely 128-bit sequences
    # NB: These sequences are defined in the SP-800-90b spec, p.44
    p_seq = np.zeros(6)
    p_seq[0] = P0 * power_bigint(P00, 127)
    p_seq[1] = P0 * power_bigint(P01, 64) * power_bigint(P10, 63)
    p_seq[2] = P0 * P01 * (power_bigint(P11, 126))
    p_seq[3] = P1 * P10 * (power_bigint(P00, 126))
    p_seq[4] = P1 * power_bigint(P10, 64) * power_bigint(P01, 63)
    p_seq[5] = P1 * power_bigint(P11, 127)

    # Step 4
    p_max = np.max(p_seq)
    min_entropy = -np.log2(p_max) / 128
    min_entropy = min(min_entropy, 1)

    return TestResult(False, None, min_entropy)
