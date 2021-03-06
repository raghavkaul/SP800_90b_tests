import logging
import numpy as np
from collections import Counter
from numbers import Integral

from utils import *
from errors import InsufficientData

__all__ = [
    "bitwise_resize",
    "encode_distinct",
]


# Operations to support
# [DONE] Given an input stream of integers or a bitstring, take chunks of it given a bitwidth
# [DONE] Given an input stream of floats, strings, or other categoricals, convert it to a
#   stream of integers or bitstrings
# Express the fact that some tests can take strings and others can't
# [DONE] Be appropriately noisy when data is changing sizes in a good or bad way, and how it affects entropy
# Push errors/warnings/logs into the type system instead of at runtime.


def _to_bitstring(symbols: DataSequence, width: int) -> str:
    assert width > 0, str(width)
    assert isinstance(width, Integral), str(width)
    return "".join(format(sym, f"0{width}b") for sym in symbols)


def bitwise_resize(
    symbols: DataSequence, new_bitwidth: int, input_width: int = -1
) -> DataSequence:
    """
    Given an input sequence of some symbols, treat the symbols as a bitstream
    and return a new list of symbols drawn from the stream at a different bit
    width/size.

    :param symbols: Symbols to translate into a bit stream and resize.
    :param new_bitwidth: Width of symbol to extract from bitstream.
    :param input_width: Width of input symbol. Only used to determine padding.
    """
    # TODO: Should suggest coalesce() if max > len?
    # TODO: This is O(n) overhead, just for an error message.
    num_unique_symbols = len(np.unique(symbols))
    bits_needed_for_data = np.ceil(np.log2(num_unique_symbols)).astype(int)
    if bits_needed_for_data <= 0:
        raise InsufficientData(
            f"Insufficient data to perform a bitwise resize (N={num_unique_symbols} L = {len(symbols)})."
        )

    if bits_needed_for_data > input_width:
        if input_width > 0:
            logging.warning(
                f"Specified data width {input_width} was likely inaccurate;"
                f"there are {num_unique_symbols} distinct symbols in the input "
                f"requiring >={bits_needed_for_data} bits to represent. "
                f"Assuming input size to be {bits_needed_for_data} bits."
            )

        input_width = bits_needed_for_data

    elif input_width > bits_needed_for_data:
        logging.debug(f"Padding data to {input_width} bits.")

    data = _to_bitstring(symbols, input_width)

    if input_width > new_bitwidth:
        if input_width % new_bitwidth != 0:
            logging.warning(
                "Bitwise resizing by a width that's not a multiple of the "
                "original bitwidth will scramble the input data. E.g.: \n"
                "[1111 0000 0111]/3bits -> [111 100 000 111]. Miscounting the "
                "number of duplicates means estimated entropy won't be reliable."
            )
        else:
            logging.info(
                "Resizing individual symbols into multiple symbols. This "
                "increases the amount of symbols, but decreases entropy. If "
                "split('C') = 'A'|'B', then, e.g., 'A' predicts -> 'B'."
            )
    elif input_width < new_bitwidth:
        # TODO: Should output also have padding? Or just get segments of the input?
        if new_bitwidth % input_width != 0:
            logging.warning(
                "Bitwise resizing by a width that's not a multiple of the "
                "original bitwidth will scramble the input data. E.g.: \n"
                "[111 100 000 111]/4bits -> [1111 0000 0111]. Ignoring real "
                "duplicate values means estimated entropy won't be reliable."
            )
        else:
            logging.info(
                "New symbols are big enough to capture several input symbols. "
                "This effectively reduces the amount of symbols, making a "
                "symbol less probable thereby appearing more entropic."
            )

    logging.debug(f"Resizing data to {new_bitwidth} bits.")
    return [
        int(data[i - new_bitwidth : i], 2)
        for i in range(new_bitwidth, len(data) + 1, new_bitwidth)
    ]


# When encoding categoricals as packed int symbols, should values that are
# outside of a specified range be A) skipped or B) assigned to a default value?


def encode_distinct(
    values: SymbolSequence, max_distinct_values: int = None, start: int = 0,
) -> DataSequence:
    """ Create an encoder to map CTI data to a numerical value.

    Because we are measuring entropy of a categorical variable instead of a
    discrete variable, we need to map data to a numerical representation.
    """

    if max_distinct_values is None:
        max_distinct_values = bitwidth_of_symbols(values)

    # Get top N unique values by counts
    unique_values_counted = sorted(
        Counter(values).most_common(max_distinct_values),
        key=lambda kv: kv[1],  # Sort by count
        reverse=True,  # Most common first
    )

    encoder_sz = len(unique_values_counted)

    # If this symbol doesn't have en encoding, replace it with this:
    # (This happens if there are more symbols than we can fit into a bitvector)
    if encoder_sz < max_distinct_values:
        start += 1
        encoder_sz -= 1
        encoding_for_unassigned_data = 0
    else:
        # If we don't have space in our encoder for any default values,
        # drop unencodable values
        encoding_for_unassigned_data = None

    end = start + encoder_sz

    # Create an encoder, assigning most frequently-seen values lower codes.
    encoder = dict(
        zip([val for (val, count) in unique_values_counted], range(start, end))
    )

    # If data is not found in the encoder, use the default val. handler
    result = []
    for value in values:
        encoded = encoder.get(value, encoding_for_unassigned_data)
        if encoded is not None:  # value couldn't fit into encoder
            result.append(encoded)
    return result
