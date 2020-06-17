import logging
import math
from collections import Counter

from utils import *
from errors import CannotCompute


def ttuple(symbols: SymbolSequence, threshold=35) -> TestResult:
    L = len(symbols)

    # Step 1: Find the largest t such that the number of t-tuples of symbols
    # is >= `threshold`
    t = None
    p_max = -math.inf

    for i in range(1, L):
        # Step 2: Let Q[i] := occurrences of most common i-tuple for i in [1, t]
        most_frequent_i_tupl, Q_i = (
            Counter([tuple(symbols[ndx : ndx + i]) for ndx in range(L - i + 1)])
            .most_common(1)
            .pop()
        )

        # logging.debug(
        #     f"Most common {i}-tuple ({Q_i} occurrences): {most_frequent_i_tupl}"
        # )

        if Q_i >= threshold:
            t = i
            # Step 3: Estimate maximum individual t-tuple probability
            # This is a "sample" probability (because we never get the full source
            # of any entropy data).
            P_i = (Q_i / (L - i + 1)) ** (1 / i)
            p_max = max(p_max, P_i)

    if t is None:
        raise CannotCompute(f"Couldn't find t-tuple for threshold={threshold}")

    # Step 4: pu := upper bound on most common t-tuple probability
    pu = min(
        1.0, p_max + (2.576 * math.sqrt((p_max * (1.0 - p_max) / (L - 1.0))))
    )

    min_entropy_per_symbol = -math.log(pu, 2.0)
    min_entropy = min_entropy_per_symbol

    # logger.debug(f"   pu                   {pu}")
    # logger.debug(f"   Symbol Min Entropy   {min_entropy_per_symbol}")
    # logger.debug(f"   Min Entropy per bit  {min_entropy}")

    return TestResult(False, None, min_entropy)
