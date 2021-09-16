class OpmlReadError(Exception):
    """This exception is thrown when a blocking OPML-related read error is encountered."""
    pass


class OpmlWriteError(Exception):
    """This exception is thrown when a blocking OPML-related write error is encountered."""
    pass
