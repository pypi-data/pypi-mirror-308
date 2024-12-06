"""Base module for setting up a logger using the SciJava LogService."""

import logging

from .handler import SciJavaLogHandler

# This will get the root-logger, thus all settings will affect all child loggers
# unless they are explicitly configured different. We could consider to (maybe
# optionally) return a package-specific logger by using getLogger(__name__),
# allowing the calling code to adjust its very own log level only.
LOG = logging.getLogger()

def setup_scijava_logger(sjlogservice):
    """Wrapper to add the SciJava handler to the logger.

    Parameters
    ----------
    sjlogservice : org.scijava.log.LogService
        The LogService instance, usually retrieved in a SciJava script by using
        the script parameters annotation '#@ LogService logs' or equivalent.

    Returns
    -------
    log : logging.Logger
        The Python logger object.
    """
    LOG.addHandler(SciJavaLogHandler(sjlogservice))
    return LOG
