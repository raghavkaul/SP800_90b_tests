import math

from utils import *

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


def multi_mmc_prediction(S: DataSequence, D=16):
    # logger.debug("MULTI MMC PREDICTION Test")
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
    N = L - 2
    subpredict = [None for x in range(D + 1)]  # add one to start index at one
    entries = [0 for x in range(D + 1)]
    maxEntries = 100000
    correct = [0 for x in range(N + 1)]

    # logger.debug("    D                    ", D)
    # logger.debug("    L                    ", L)
    # logger.debug("    N                    ", N)

    # step 2
    M = [dict() for x in range(D + 1)]

    # step 3
    scoreboard = [0 for x in range(D + 1)]
    winner = 1

    # logger.debug("    STEP 4")
    # step 4
    ys = list()
    for i in range(3, L + 1):
        for d in range(1, D + 1):
            if d < (i - 1):
                x = S[i - d - 1 : i - 1]
                y = S[i - 1]
                atuple = (tuple(x), y)

                if atuple in M:
                    M[d][atuple] += 1
                else:
                    if entries[d] < maxEntries:
                        M[d][atuple] = 1
                        entries[d] += 1
                        ys.append(y)
        for d in range(1, D + 1):
            if d < i:
                # find y corresponding to highest M[Si-d,...,Si-2,y]
                ymax = -10
                maxtuple = None
                for atuple in M[d]:
                    if M[d][atuple] > ymax:
                        maxtuple = atuple
                        ymax = M[d][atuple]
                    else:
                        M[d][atuple] == ymax
                        if atuple[1] > maxtuple[1]:
                            maxtuple = atuple
                            ymax = M[d][atuple]
                subpredict[d] = ymax
                allzero = True
                for atuple in M[d]:
                    if M[d][atuple] != 0:
                        allzero = False
                        break
                if allzero:
                    subpredict[d] = None

        prediction = subpredict[winner]
        if prediction == S[i]:
            correct[i - 2] = 1

        # update scoreboard
        for d in range(1, D + 1):
            if subpredict[d] == S[i]:
                scoreboard[d] += 1
                if scoreboard[d] >= scoreboard[winner]:
                    winner = d
    # logger.debug("    STEP 5")
    # step 5
    C = 0
    for c in correct:
        if c == 1:
            C += 1

    # logger.debug("    STEP 6")
    # step 6
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

    # logger.debug("    STEP 7")
    # Step 7
    p_local = search_for_p(
        r,
        N,
        iterations=1000,
        min_plocal=0.0,
        max_plocal=1.0,
        tolerance=0.00000001,
        verbose=False,
    )

    # logger.debug("    p_local              ", p_local)

    # logger.debug("    STEP 8")
    # Step 8
    pu = max(p_prime_global, p_local, 1.0 / (2 ** 2))
    min_entropy_per_symbol = -math.log(pu, 2)
    min_entropy_per_bit = min_entropy_per_symbol

    # logger.debug("    pu                   ", pu)
    # logger.debug("    Symbol Min Entropy   ", min_entropy_per_symbol)
    # logger.debug("    Min Entropy per bit  ", min_entropy_per_bit)

    return TestResult(False, None, min_entropy_per_bit)
