__author__ = 'tanner'
class ParserError(RuntimeError):
    """Raise when the parser encounters a piece of data it can't parse. Usually from some odd edge case or when
    the data is malformed."""
    pass