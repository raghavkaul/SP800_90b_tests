import cProfile
import logging
import math
from collections import Counter

from utils import *
from errors import CannotCompute


def _most_common_ituple(symbols: SymbolSequence, i: int, L: int):
    # Step 2: Let Q[i] := occurrences of most common i-tuple for i in [1, t]
    root = Trie(None)

    # mci_start, mci_end = (None, None)
    most_frequent_leaf_count = -math.inf
    for ndx in range(L - i + 1):
        leaf_count = root.add(symbols, start=ndx, end=ndx + i)
        if leaf_count > most_frequent_leaf_count:
            most_frequent_leaf_count = leaf_count
            # mci_start, mci_end = ndx, ndx + i

    return most_frequent_leaf_count

    # print_trie(root)
    # # Find most common i-tuple
    # seq = []
    # while root.children:
    #     maximal_n_tuple = max(root.children.values(), key=lambda child: child.count)
    #     seq.append(maximal_n_tuple.val)
    #     if maximal_n_tuple.is_leaf():
    #         return tuple(seq), maximal_n_tuple.count
    #     root = maximal_n_tuple
    #
    # raise Exception("Something went wrong when computing ITUPLEs")


def ttuple(symbols: SymbolSequence, threshold=35) -> TestResult:
    L = len(symbols)

    # Step 1: Find the largest t such that the number of t-tuples of symbols
    # is >= `threshold`
    t = None
    p_max = -math.inf
    import qcore

    start = qcore.utime()
    for i in range(1, L):
        # Step 2: Let Q[i] := occurrences of most common i-tuple for i in [1, t]
        # print(f"i={i} ==================")
        # Q_i = _most_common_ituple(symbols, i, L)
        # print(f"my Qi {Q_i}")
        most_frequent_i_tupl, Q_i = (
            Counter([tuple(symbols[ndx : ndx + i]) for ndx in range(L - i + 1)])
            .most_common(1)
            .pop()
        )
        # print(f"their Qi {most_frequent_i_tupl} {Q_i}")

        # logging.debug(f"Most common {i}-tuple ({Q_i} occurrences: --")

        if Q_i >= threshold:
            t = i
            # Step 3: Estimate maximum individual t-tuple probability
            # This is a "sample" probability (because we never get the full source
            # of any entropy data).
            P_i = (Q_i / (L - i + 1)) ** (1 / i)
            p_max = max(p_max, P_i)
    # print(f"Took {(qcore.utime() - start) / qcore.MILLISECOND}ms to find t-tuple")

    if t is None:
        raise CannotCompute(f"Couldn't find t-tuple for threshold={threshold}")

    # Step 4: pu := upper bound on most common t-tuple probability
    pu = min(1.0, p_max + (2.576 * math.sqrt((p_max * (1.0 - p_max) / (L - 1.0)))))

    min_entropy_per_symbol = -math.log(pu, bitwidth_of_symbols(symbols))
    min_entropy = min_entropy_per_symbol

    return TestResult(False, None, min_entropy)
