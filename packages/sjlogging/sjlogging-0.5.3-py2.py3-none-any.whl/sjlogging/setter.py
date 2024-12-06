"""Setter functions for conveniently adjusting the log level in various ways."""

from .logger import LOG


def set_loglevel(levelname):
    """Wrapper function to set the log level by name.

    Parameters
    ----------
    levelname : str
        One from "CRITICAL", "ERROR", "WARNING", "INFO", "DEBUG".
    """
    level = 30  # set the default level
    mapping = {
        "CRITICAL" : 50,
        "ERROR"    : 40,
        "ERR"      : 40,
        "WARNING"  : 30,
        "WARN"     : 30,
        "INFO"     : 20,
        "DEBUG"    : 10,
    }
    if levelname in mapping:
        level = mapping[levelname]
    LOG.setLevel(level)


def set_loglevel_scijava_style(levelnumber):
    """Wrapper to set the Python log level using the SciJava level numbers.

    A convenience method that allows for setting the log level by using the
    numbers used in the SciJava LogService class. The mapping happens as
    described by this scheme:

    SciJava level (value) -> Python logging level
    ---------------------------------------------
    ERROR (1) -> 40
    WARN (2)  -> 30
    INFO (3)  -> 20
    DEBUG (4) -> 10
    TRACE (5) -> 10  (same as DEBUG since Pythong doesn't have a TRACE level)

    Parameters
    ----------
    levelnumber : int
        Numeric value ranging from 1 to 5. Will fall back to WARNING level if
        the number is not within the defined range.
    """
    level = 30  # set the default level
    if levelnumber > 0 and levelnumber <= 5:
        level = (5 - levelnumber) * 10
        if level == 0:
            level = 10
    LOG.setLevel(level)


def set_verbosity(count):
    """Set the logging verbosity, defaulting to "WARNING".

    This is a convenience function that wraps the calculation and setting of the
    logging level in a way that it can be directly associated with e.g. the
    number of occurences of a '-v' switch on the command line parsed by the
    argparse package. The idea is basically to do something like this:

    >>> argparser = argparse.ArgumentParser()
    >>> argparser.add('-v', '--verbosity', action='count', default=0)
    >>> args = argparser.parse_args()
    >>> set_verbosity(args.verbosity)

    Parameters
    ----------
    count : int
        An integer number between -2 and 2.
    """
    if count < -2 or count > 2:
        return
    level = (3 - count) * 10
    LOG.setLevel(level)
