import math
from typing import List, Tuple

import numpy as np

from utils import *


def pq_func(p):
    q = 1.0 - p

    z = 1.0 / q

    print(p, q, e, z)
    fq = upper_incomplete_gamma(3, z) * (z ** (-3.0)) * (e ** z)

    result = (p * (q ** -2.0)) * (1.0 + (0.5 * ((1 / p) - (1 / q)))) * fq
    result = result - ((p * (q ** -1.0)) * 0.5 * ((1 / p) - (1 / q)))

    return result


def _runs_between_collisions(data: DataSequence) -> List[Tuple[int, int]]:
    i = 0
    runs_between_collisions = []
    while i < len(data):
        j = i + 1

        seen = {data[i]}

        while j < len(data):
            if data[j] in seen:
                runs_between_collisions.append((i, j))
                # runs_between_collisions.append((seen[data[j]], j))
                break

            seen.add(data[j])
            # seen[data[j]] = j

            j += 1

        i = j + 1

    return runs_between_collisions


def collision(data: DataSequence) -> TestResult:
    # FIXME: Non-standard results if data is non-binary

    runs = _runs_between_collisions(data)

    run_lengths = [run[1] - run[0] + 1 for run in runs]
    rl_avg = np.mean(run_lengths)
    rl_stdev = np.std(
        run_lengths, ddof=1
    )  # Any entropy-measurable source is necessarily "sampled," hence ddof=1.
    rl_avg_lowerbound = rl_avg - (
        2.576 * (rl_stdev / np.sqrt(len(run_lengths)))
    )

    print(rl_avg, rl_stdev, rl_avg_lowerbound)

    # Step 7
    iterations = 1000
    iteration = 0
    last_p_mid = -1.0
    p_min = 0.5
    p_mid = 0.75
    p_max = 1.0

    found = False
    while not found:
        candidate = pq_func(p_mid)
        if candidate > rl_avg_lowerbound:
            p_min = p_mid
            p_mid = (p_min + p_max) / 2.0
        elif candidate < rl_avg_lowerbound:
            p_max = p_mid
            p_mid = (p_min + p_max) / 2.0
        elif (candidate == rl_avg_lowerbound) or (p_mid == last_p_mid):
            found = True
            p = p_mid
            break
        last_p_mid = p_mid

        iteration += 1
        if iteration > iterations:
            found = False
            break
    # step 8

    if found:
        if p < 0.5:
            p = 1.0 - p
        print("   p =", p)
        min_entropy = -math.log(p, 2.0)
        print("   min_entropy =", min_entropy)
    else:
        print("   p = 0.5")
        min_entropy = 1.0
        print("   min_entropy = 1.0")

    return TestResult(False, None, min_entropy)
