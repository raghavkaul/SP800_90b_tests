class CannotCompute(Exception):
    """ Cannot compute this test over this data. """

    pass


class UnsupportedDatatype(Exception):
    """ This test cannot handle this type of data. """

    pass
