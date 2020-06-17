import math

from collections import Counter
from utils import *


def mcv(data: DataSequence) -> TestResult:
    """
    Returns min-entropy estimate from mcv test.

    :param data to calculate estimate for

    From standards doc (p. 41):
    This method first finds the proportion of the most common value in the
    input dataset, and then constructs a confidence interval for this
    proportion. The upper bound of the confidence interval is used to estimate
    the min-entropy per sample of the source.

    """
    L = len(data)

    # 1. Find the proportion of the most-common value (p-hat) in the dataset
    most_common_val, mcv_count = Counter(data).most_common(1).pop()
    p_hat = mcv_count / L

    # 2. Calculate an upper bound on the probability (p-sub-u) of the most common value
    p_u = p_hat + (2.576 * math.sqrt((p_hat * (1 - p_hat)) / (L - 1)))
    p_u = min(1.0, p_u)

    # 3. The estimated min-entropy is -log2(p-sub-u)
    min_entropy = -math.log2(p_u)
    return TestResult(False, None, min_entropy)
