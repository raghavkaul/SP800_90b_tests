import math
import numpy as np
from collections import defaultdict

from utils import *
from errors import InsufficientData

precision = 300


def lz78y(S: DataSequence, B=16):
    # Step 1
    L = len(S)
    N = L - B - 1

    if N <= 0:
        raise InsufficientData(f"Need >{B + 1} samples for lz78y test.")

    correct = np.zeros(N + 1)
    MAX_DICT_SZ = 2 ** 16

    # Step 2
    # Map[Data Subsequence -> Map[Subsequent Character, Count]]
    D = defaultdict(lambda: defaultdict(lambda: -1))
    S.insert(0, 0)

    # Step 3. Given a run of data, add it to a dictionary of predictions
    # This dictionary is loosely based on lz78 Yabba encoding
    for i in range(B + 2, L + 1):
        for j in range(B, 0, -1):
            # NB: tuples "hash" (freeze) lists for dictionary keys
            substr = tuple(S[i - j - 1 : i - 1])
            if substr not in D and len(D) >= MAX_DICT_SZ:
                continue
            D[substr][S[i - 1]] += 1

        # 3b
        prediction = None
        maxcount = -1
        for j in range(B, 0, -1):
            preceding_seq = tuple(S[i - j : (i - 1) + 1])
            if preceding_seq in D:
                # TODO: Handle ties
                likeliest, count = max(
                    D[preceding_seq].items(), key=lambda kv: kv[1]
                )

                if count > maxcount:
                    maxcount = count
                    prediction = likeliest

        if prediction == S[i]:
            correct[i - B - 1] = 1

    # Step 4. Calculate the predictor's global performance (P_global)
    # and the upper-bound of its' confidence interval
    correct_prediction_locs = np.nonzero(correct)[0]
    num_correct = len(correct_prediction_locs)

    P_global = num_correct / N

    if P_global == 0:
        P_global = 1 - (0.01 ** (1 / N))
    else:
        P_global += 2.576 * (np.sqrt((P_global * (1 - P_global)) / (N - 1)))

    # Step 5. Calculate the predictor's local performance, based on the longest
    # run of correct predictions.
    longest_runlen = 0
    runlen = 1
    for i in range(1, len(correct_prediction_locs)):
        if correct_prediction_locs[i - 1] == correct_prediction_locs[i]:
            runlen += 1
            longest_runlen = max(longest_runlen, runlen)
        else:
            runlen = 1

    # Let r be one greater than the length of the longest run of ones in `correct`
    r = longest_runlen + 1

    #   iteratively find Plocal
    p_local = search_for_p(
        r,
        N,
        iterations=1000,
        min_plocal=0.0,
        max_plocal=1.0,
        tolerance=0.00000001,
    )

    # logger.debug("    p_local              ", p_local)

    # Step 6
    pu = max(P_global, p_local, 1.0 / 4)  # 4 = 2 ** (symbolLength=2)
    min_entropy_per_symbol = -math.log(pu, 2)
    min_entropy_per_bit = min_entropy_per_symbol

    # logger.debug("    pu                   ", pu)
    # logger.debug("    Symbol Min Entropy   ", min_entropy_per_symbol)
    # logger.debug("    Min Entropy per bit  ", min_entropy_per_bit)

    return TestResult(False, None, min_entropy_per_bit)
