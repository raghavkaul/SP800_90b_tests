import math

from .utils import *


def mcv(bits, symbol_length, verbose=True):
    logger.debug("MCV Test")
    bitcount = len(bits)
    L = bitcount // symbol_length

    # logger.debug(bits)
    logger.debug("  Symbol Length        ", symbol_length)
    logger.debug("  Number of bits       ", (L * symbol_length))
    logger.debug("  Number of Symbols    ", L)
    # Make Frequency Table
    freq_table = list()
    for i in range(2 ** symbol_length):
        freq_table.append(0)

    # Build the frequency table
    # Keep track of the most frequent symbol
    biggest = 0
    biggest_symbol = 0
    for i in range(L):
        symbol_bits = bits[i * symbol_length : ((i + 1) * symbol_length)]
        symbol = int(symbol_bits, 2)
        # print (" symbol:",symbol," symbol_bits",symbol_bits)
        # logger.debug(symbol_bits,symbol)
        freq_table[symbol] += 1
        if freq_table[symbol] > biggest:
            biggest = freq_table[symbol]
            biggest_symbol = symbol

    logger.debug("  Most common symbol   ", biggest_symbol)

    # do the SP800-90b section 6.3.1 sums
    p_hat = biggest / L
    logger.debug("  p_hat                ", p_hat)

    pu = p_hat + (2.576 * (math.sqrt((p_hat * (1.0 - p_hat)) / (L - 1.0))))
    if pu > 1.0:
        pu = 1.0
    min_entropy_per_symbol = -math.log(pu, 2.0)
    min_entropy = (-math.log(pu, 2.0)) / symbol_length
    logger.debug("  pu                   ", pu)
    logger.debug("  Symbol Min Entropy   ", min_entropy_per_symbol)
    logger.debug("  Min Entropy per bit  ", min_entropy)

    return (False, None, min_entropy)
