import logging
from math import inf, isclose
from mpmath import power as exp
import numpy as np
from typing import List, Tuple

from utils import *
from encoders import bitwise_resize
from errors import CannotCompute


def F(z):
    return upper_incomplete_gamma(3, z) * exp(z, -3) * exp(e, z)


def _search_for_p(X_bar_goal, bounds=(0.5, 1), previous_err=inf, max_iter=100):
    """

    :param X_bar_goal:
    :param bounds:
    :param previous_err:
    :param max_iter:
    :return:
    """
    p_closest, err_p_closest = (None, inf)
    lbound, rbound = bounds

    i = 0
    while i < max_iter:
        p = (lbound + rbound) / 2
        q = 1 - p
        z = exp(q, -1)

        X_bar_computed = p * exp(q, -2)
        X_bar_computed *= 1 + 0.5 * (exp(p, -1) - exp(q, -1))
        X_bar_computed *= F(z)
        X_bar_computed -= (p * exp(q, -1)) * 0.5 * (exp(p, -1) - exp(q, -1))

        # Flogging.debug(
        #     f"p, q=({p}, {q}); X̄={X_bar_computed} (goal={X_bar_goal})"
        # )

        if isclose(X_bar_goal, X_bar_computed):
            return p
        elif X_bar_computed > X_bar_goal:
            lbound = p
        elif X_bar_computed < X_bar_goal:
            rbound = p

        err = abs(X_bar_computed - X_bar_goal)

        if err < err_p_closest:
            # This is the closest we have to a result thus far
            # If the search terminates unsuccessfully, see if this would be appropriate
            p_closest, err_p_closest = p, err

        if isclose(err, previous_err) or err > previous_err:
            # logging.debug("Search for an appropriate p-val diverged.")
            pass

        previous_err = err

        i += 1

    if p_closest and err_p_closest < 0.1:
        # logging.debug(
        #     "Didn't find an actual match for p; returning an approximate."
        # )
        return p_closest

    raise CannotCompute(f"Couldn't find p within {max_iter} iterations.")


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
    data = bitwise_resize(data, 1)

    runs = _runs_between_collisions(data)

    run_lengths = [run[1] - run[0] + 1 for run in runs]
    rl_avg = np.mean(run_lengths)
    rl_stdev = np.std(
        run_lengths, ddof=1
    )  # Any entropy-measurable source is necessarily "sampled," hence ddof=1.
    rl_avg_lowerbound = rl_avg - (
        2.576 * (rl_stdev / np.sqrt(len(run_lengths)))
    )

    # TODO: Catch CannotCompute? Check whether to scale H_min by bitlength
    p = _search_for_p(X_bar_goal=rl_avg_lowerbound)
    min_entropy = -np.log2(p)

    return TestResult(False, None, min_entropy)
