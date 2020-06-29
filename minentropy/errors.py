class CannotCompute(Exception):
    """ Cannot compute this test over this data. """

    pass


class InsufficientData(CannotCompute):
    """ Can't perform this operation because there's not enough data to measure. """

    pass


class UnsupportedDatatype(Exception):
    """ This test cannot handle this type of data. """

    pass
