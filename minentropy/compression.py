import math

from utils import *

from errors import *


def F(z, t, u):
    if u < t:
        return (z ** 2.0) * ((1.0 - z) ** (u - 1.0))
    if u == t:
        return z * ((1.0 - z) ** (t - 1.0))


# The equations in step 7 of 6.3.4 are downright misleading and do not work.
# This function more or less follows what NIST did in their code but it looks
# nothing like the equations in the spec.
def G(z, v, d, L):
    g_sum = 0.0
    st = [
        math.log(u, 2.0) * ((1.0 - z) ** (u - 1.0))
        for u in range((d + 1), v + d + 1)
    ]
    g_sum = (
        v
        * z
        * z
        * sum(
            [
                math.log(u, 2.0) * ((1.0 - z) ** (u - 1.0))
                for u in range(1, (d + 1))
            ]
        )
    )
    g_sum += z * z * sum([(v - t - 1) * st[t] for t in range(v - 1)])
    g_sum += z * sum(st)
    return g_sum / v


from typing import List


def compression(bits: str, d=1000):
    # logger.debug("COMPRESSION Test")
    L = len(bits)

    if L < d:
        raise CannotCompute

    # # logger.debug(bits)
    # logger.debug("   Symbol Length        1")
    # logger.debug("   Number of bits      ", L)

    # step 1
    b = 6
    blocks = L // b

    s_prime = [0,] + [int(bits[b * i : b * (i + 1)], 2) for i in range(blocks)]

    # logger.debug("   Number of blocks    ", blocks)

    # Step 2
    dict_data = s_prime[1 : d + 1]
    v = blocks - d
    test_data = s_prime[d + 1 :]

    # logger.debug("   v                   ", v)

    # Step 3
    dictionary = [
        0 for i in range((2 ** b) + 1)
    ]  # Make it 1 bigger and leave the zero element dangling
    # so the indexes match the spec which uses 1 based arrays.
    for i in range(1, d + 1):
        dictionary[s_prime[i]] = i

    # Step 4
    D = [0,] + [0 for i in range(v)]
    for i in range(d + 1, blocks + 1):
        # # logger.debug("  i = ",i,end="")
        # # logger.debug("  s_prime[%d]=" % i,s_prime[i])
        if dictionary[s_prime[i]] != 0:
            # print ("D[i-d] = D[%d - %d] = D[%d]" % (i,d,i-d))
            D[i - d] = i - dictionary[s_prime[i]]
            dictionary[s_prime[i]] = i
        if dictionary[s_prime[i]] == 0:
            dictionary[s_prime[i]] = i
            D[i - d] = i

    # Step 5

    x_sum = 0.0
    for i in range(1, v + 1):
        # # logger.debug("   D[",i,"] = ",D[i], "log2(D[i])=",math.log(D[i],2))
        x_sum += math.log(D[i], 2)
    x_bar = x_sum / v

    # logger.debug("   x_bar               ", x_bar)

    c = 0.5907

    s_sum = 0.0
    for i in range(1, v + 1):
        s_sum += math.log(D[i], 2) ** 2
    s_sum = s_sum / (v - 1.0)
    s_sum = s_sum - (x_bar ** 2)
    sigma_hat = c * math.sqrt(s_sum)

    # logger.debug("   sigma_hat           ", sigma_hat)

    # Step 6

    x_bar_prime = x_bar - ((2.576 * sigma_hat) / math.sqrt(v))
    # logger.debug("   x_bar_prime         ", x_bar_prime)

    # Step 7

    p_min = 2.0 ** -b  # binary search bounds
    p_max = 1.0
    p_mid = (p_min + p_max) / 2.0

    # logger.debug("   p_min               ", p_min)
    # logger.debug("   p_max               ", p_max)
    iterations = 1000
    iteration = 0

    found = False
    while iteration < iterations:
        q = (1.0 - p_mid) / ((2.0 ** b) - 1.0)
        candidate = G(p_mid, v, d, L) + (((2.0 ** b) - 1.0) * G(q, v, d, L))

        if abs(candidate - x_bar_prime) < 0.00000000001:
            found = True
            break
        elif candidate > x_bar_prime:
            p_min = p_mid
            p_mid = (p_min + p_max) / 2.0
        elif candidate < x_bar_prime:
            p_max = p_mid
            p_mid = (p_min + p_max) / 2.0

        iteration += 1

    print("   p          =", p_mid)
    # Step 8
    if found:
        min_entropy = -math.log(p_mid, 2) / b
        # logger.debug("   min_entropy =", min_entropy)
        return TestResult(False, None, min_entropy)
    else:
        min_entropy = 1.0
        # logger.debug("   min_entropy = 1.0")
        return TestResult(False, None, min_entropy)
