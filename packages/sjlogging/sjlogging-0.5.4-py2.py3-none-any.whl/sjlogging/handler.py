"""Logging handler class redirecting messages to SciJava's LogService."""

import logging


class SciJavaLogHandler(logging.StreamHandler):

    """A logging handler for routing messages to the SciJava LogService.

    This class provides an easy way to create a Handler object for Python's
    'logging' package that will re-route messages to the [SciJava][1]
    LogService.

    [1]: https://github.com/scijava/scijava-common/
    """

    def __init__(self, sjlog):
        """Initialize the logging handler for the SciJava logging.

        Parameters
        ----------
        sjlog : org.scijava.log.LogService
            The LogService instance, usually retrieved in a script by using the
            SciJava script parameters annotation '#@ LogService logs' or
            equivalent.
        """
        super(SciJavaLogHandler, self).__init__()
        self.sjlog = sjlog

    def emit(self, record):
        """Call the corresponding SciJava logging method.

        Before the log message is handed over to the SciJava LogService we make
        sure the log-level of that very service is set accordingly.

        Rationale:

        All the level-handling for a given message has already been done by the
        Python logging filters etc., so once the emit() method is called we *do*
        know this message should actually be put out. Hence we first remember
        the current SciJava log level, adjust it according to the level of the
        given record, then we call the corresponding LogService `log()` method and
        finally we re-set the SciJava log level to the value it had when this
        method was called.
        """
        # remember the current LogService level:
        sjlevel = self.sjlog.getLevel()

        formatted = self.format(record)

        if record.levelname == "DEBUG":
            self.sjlog.setLevel(4)
            self.sjlog.log(4, formatted)
        elif record.levelname == "INFO":
            self.sjlog.setLevel(3)
            self.sjlog.log(3, formatted)
        elif record.levelname == "WARNING":
            self.sjlog.setLevel(2)
            self.sjlog.log(2, formatted)
        else:  # everything else, including "ERROR" and "CRITICAL":
            self.sjlog.setLevel(1)
            self.sjlog.log(1, formatted)

        # reset the LogService level to its previous value:
        self.sjlog.setLevel(sjlevel)
