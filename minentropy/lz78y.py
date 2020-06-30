import math

from utils import *
from errors import InsufficientData

precision = 300


def p_local_func(p, r, N):

    q = 1.0 - p

    x = 1.0
    for i in range(1, 11):
        x = 1.0 + q * (p ** r) * (x ** (r + 1))
    # # logger.debug("     x : ",x)
    result = (1.0 - (p * x)) / ((r + 1.0 - (r * x)) * q)
    result = result / (x ** (N + 1))
    return result


def lz78y(S: DataSequence, B=16):
    # logger.debug("LZ78Y Test")
    L = len(S)

    # # logger.debug(bits)
    # logger.debug("    Symbol Length        ", symbol_length)
    # logger.debug("    Number of bits       ", (L * symbol_length))
    # logger.debug("    Number of Symbols    ", L)

    # Split bits into integer symbols
    #   prepend with 0, so the symbols are indexed from 1
    # # logger.debug(bits)
    S.insert(0, 0)

    # # logger.debug(S)
    # Step 1
    N = L - B - 1

    if N <= 0:
        raise InsufficientData(f"Need >{B + 1} samples for lz78y test.")

    correct = np.zeros(N + 1)
    MAX_DICT_SZ = 2 ** 16

    # Step 2
    D = dict()
    dictionarySize = 0

    # Step 3
    # logger.debug(
    #     "    ",
    #     "i".ljust(4),
    #     "Add to D".ljust(20),
    #     "prev".ljust(14),
    #     "Max D[prev]".ljust(16),
    #     "prediction".ljust(12),
    #     "Si".ljust(4),
    #     "Correct_i-b-1",
    # )
    for i in range(B + 2, L + 1):
        add_to_d = list()
        prevlist = list()
        maxdlist = list()

        for j in range(B, 0, -1):
            # 3a
            ss = tuple(S[i - j - 1 : (i - 2) + 1])

            if (ss not in D) and (dictionarySize < maxDictionarySize):
                D[ss] = dict()
                D[ss][S[i - 1]] = 0
                add_to_d.append("D[" + str(ss) + "][" + str(S[i - 1]) + "]")
                dictionarySize += 1
            if ss in D:
                if S[i - 1] not in D[ss]:
                    D[ss][S[i - 1]] = 0
                    add_to_d.append("D[" + str(ss) + "][" + str(S[i - 1]) + "]")
                D[ss][S[i - 1]] = D[ss][S[i - 1]] + 1

        # 3b
        prediction = None
        maxcount = None
        for j in range(B, 0, -1):
            prev = tuple(S[i - j : (i - 1) + 1])
            prevlist.append(str(prev))
            if prev in D:
                maxyval = 0

                for cy in range(4):  # 4 = 2 ** (symbol_length = 2)
                    if cy in D[prev]:
                        if D[prev][cy] >= maxyval:
                            maxyval = D[prev][cy]
                            y = cy
                if (maxcount == None) or (D[prev][y] > maxcount):
                    prediction = y
                    maxcount = D[prev][y]
                    maxdlist.append(maxcount)
        if prediction == S[i]:
            correct[i - B - 1] = 1

        # print out table line
        # # logger.debug(add_to_d)
        # # logger.debug(prevlist)
        # # logger.debug(maxdlist)
        # if verbose:
        #    for pad in range(20):
        #        add_to_d.append("-")
        #        prevlist.append("-")
        #        maxdlist.append("-")
        #    for line in range(4):
        #        if line == 0:
        #            # logger.debug("    ",str(i).ljust(4),add_to_d[line].ljust(20), prevlist[line].ljust(14), str(maxcount).ljust(16),
        #                        str(prediction).ljust(12),str(S[i]).ljust(4), correct[i-B-1])
        #        else:
        #            # logger.debug("    "," ".ljust(4),add_to_d[line].ljust(20), prevlist[line].ljust(14), str(maxcount).ljust(16),
        #                        " ".ljust(12)," ".ljust(4), " ")
    # step 4
    # C = sum(correct)
    C = 0
    for i in correct:
        if i == 1:
            C += 1

    # # logger.debug("    correct              ",correct)
    p_global = float(C) / float(N)
    if p_global == 0:
        p_prime_global = 1 - (0.001 ** (1.0 / N))
    else:
        p_prime_global = min(
            1.0,
            p_global
            + (2.576 * math.sqrt((p_global * (1.0 - p_global)) / (N - 1.0))),
        )

    # logger.debug("    p_global             ", p_global)
    # logger.debug("    p_prime_global       ", p_prime_global)

    # Step 5
    #  Find run of longest ones in correct, to find r

    rlen = 0
    currentlen = 0
    for x in correct:
        if x != 1:
            currentlen = 0
        else:
            currentlen += 1
            if currentlen > rlen:
                rlen = currentlen
    r = 1 + rlen

    # logger.debug("    C                    ", C)
    # logger.debug("    r                    ", r)

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
    pu = max(p_prime_global, p_local, 1.0 / 4)  # 4 = 2 ** (symbolLength=2)
    min_entropy_per_symbol = -math.log(pu, 2)
    min_entropy_per_bit = min_entropy_per_symbol

    # logger.debug("    pu                   ", pu)
    # logger.debug("    Symbol Min Entropy   ", min_entropy_per_symbol)
    # logger.debug("    Min Entropy per bit  ", min_entropy_per_bit)

    return TestResult(False, None, min_entropy_per_bit)
