import math

from utils import *
from errors import CannotCompute


def ttuple(symbols: Data, threshold=35) -> TestResult:
    L = len(symbols)

    # # logger.debug(bits)
    # logger.debug(f"   Symbol Length       {symbol_length}")
    # logger.debug(f"   Number of bits       {(L * symbol_length)}")
    # logger.debug(f"   Number of Symbols    {L}")
    # logger.debug(f"   t-threshold = {threshold}")

    # Steps 1 and 2
    # Find-t
    # The t-tuple length for which the count is at least 35
    tuple_dict = dict()
    Q = [0 for x in range(1024)]  # Large enough to always be big enough
    P = [0 for x in range(1024)]  # Large enough to always be big enough
    P_max_array = [
        0 for x in range(1024)
    ]  # Large enough to always be big enough
    last_five_maxes = [
        threshold + 100 for i in range(5)
    ]  # Keep track of the last 10. If they were all one,
    # end to loop to save compute time.
    for t in range(
        1, min(L + 1, 128)
    ):  # (max_count == None) or (max_count > threshold):
        max_count = 0
        # logger.debug(f"   Testing t={t}")
        tuple_position_count = 1 + L - t
        # # logger.debug("   Searching through ",tuple_position_count," positions")

        for i in range(tuple_position_count):
            the_tuple = tuple(symbols[i : i + t])
            if the_tuple in tuple_dict:
                tuple_dict[the_tuple] += 1
            else:
                tuple_dict[the_tuple] = 1

            if tuple_dict[the_tuple] > max_count:
                max_count = tuple_dict[the_tuple]
                max_tuple = the_tuple
            # print ("   Found ",the_tuple," at location ",i," count = ",tuple_dict[the_tuple])
        Q[t] = max_count
        last_five_maxes = last_five_maxes[1:]
        last_five_maxes.append(max_count)
        # logger.debug(f"   max tuple count: {max_count}")
        if (max(last_five_maxes) == 1) or (
            max(last_five_maxes) < (threshold - 10)
        ):
            break
        # # logger.debug("   Q[t] = ",max_count, "  Q[i]=",Q[1:t+1])

    found = False
    for pos, qt in reversed(list(enumerate(Q[: L + 1]))):
        # # logger.debug("   pos=",pos, "  qt=",qt)
        if qt >= threshold:
            found = True
            t = pos
            break

    if not found:
        raise CannotCompute("No t found.")

    # Step 2
    for i in range(1, t + 1):
        P[i] = Q[i] / (L - i + 1.0)
        P_max_array[i] = P[i] ** (1.0 / i)
    p_max = max(P_max_array)

    pu = min(
        1.0, p_max + (2.576 * math.sqrt((p_max * (1.0 - p_max) / (L - 1.0))))
    )

    min_entropy_per_symbol = -math.log(pu, 2.0)
    min_entropy = min_entropy_per_symbol

    # logger.debug(f"   pu                   {pu}")
    # logger.debug(f"   Symbol Min Entropy   {min_entropy_per_symbol}")
    # logger.debug(f"   Min Entropy per bit  {min_entropy}")

    return TestResult(False, None, min_entropy)
