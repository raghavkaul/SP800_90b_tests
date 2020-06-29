from collections import Counter
import math
import logging
import scipy.special as sc

from utils import *
from errors import CannotCompute

nCr = sc.comb


def lrs(data: SymbolSequence, threshold=35):
    L = len(data)

    # Step 1: Find smallest u s.t. Q[u] < 35
    u = v = None
    Q_i_prev = -math.inf
    P_max = -math.inf

    for i in range(1, L):
        # Step 2: Let Q[i] := num occurrences of most common i-tuple for i in [1, t]
        i_tupls = [tuple(data[ndx : ndx + i]) for ndx in range(L - i + 1)]
        i_tuples_counted = Counter(i_tupls)
        most_frequent_i_tupl, Q_i = i_tuples_counted.most_common(1).pop()

        # logging.debug(
        #     f"Most common {i}-tuple ({Q_i} occurrences): {most_frequent_i_tupl}"
        # )

        if Q_i < threshold:
            if u is None:
                u = i

        if Q_i == 1 and Q_i_prev is not None and Q_i_prev >= 2:
            v = i - 1

        if u is not None and v is None:
            # Step 3: Compute W-tuple collision probability
            # logging.debug(f"{i}-tupls to count: {i_tuples_counted}")
            P_w = sum(
                nCr(count_i, 2) for count_i in i_tuples_counted.values()
            ) / nCr(L - i + 1, 2)
            # logging.debug(f"P_{i} = {P_w}")

            P_max_w = P_w ** (1 / i)
            # logging.debug(f"P_max_{i} = {P_max_w}")
            P_max = max(P_max, P_max_w)

        Q_i_prev = Q_i

    # logging.debug(f"u={u} v={v}")

    if v is None or v < u:
        raise CannotCompute

    # Step 4: pu := upper bound on most common t-tuple probability
    p_u = min(1.0, upper_probability_bound(P_max, L))

    min_entropy_per_symbol = -math.log(p_u, 2.0)
    min_entropy = min_entropy_per_symbol

    return TestResult(False, None, min_entropy)
