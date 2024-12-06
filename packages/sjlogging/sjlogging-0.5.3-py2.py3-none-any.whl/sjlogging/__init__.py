"""SciJava log handler for Python

A very thin Python package (mavenized for [ImageJ2][imagej]) to use the
[SciJava][gh_scijava] [LogService][gh_sj_logservice] as a handler for
[Python's logging facility][py_logging]. See the wiki page about
[Logging][ij_logging] for more details about ImageJ's logging framework.

Developed and provided by the [Imaging Core Facility (IMCF)][imcf] of the
Biozentrum, University of Basel, Switzerland.

# Example usage

The snippet below demonstrate how to use the handler in an ImageJ2 Python script
utilizing the fabulous [Script Parameters][ij_script_params].

```Python
#@ LogService sjlogservice

from sjlogging.logger import setup_scijava_logger
from sjlogging.setter import set_loglevel


def log_messages(level):
    log.critical("+++ new round of messages (level %s) +++" % level)
    set_loglevel(level)
    log.debug('debug log message')
    log.info('info log message')
    log.warn('warn log message')
    log.error('error log message')
    log.critical('critical log message')
    log.critical("--- finished round of messages (level %s) ---" % level)


log = setup_scijava_logger(sjlogservice)

log_messages('WARNING')
log_messages('INFO')
log_messages('DEBUG')
log_messages('WARNING')
```


[imcf]: https://www.biozentrum.unibas.ch/imcf
[imagej]: https://imagej.net
[ij_logging]: https://imagej.net/Logging
[py_logging]: https://docs.python.org/2/library/logging.html
[gh_scijava]: https://github.com/scijava
[gh_sj_logservice]: https://github.com/scijava/scijava-common/tree/master/src/main/java/org/scijava/log
"""

from .logger import setup_scijava_logger as setup_logger
from .setter import set_loglevel, set_loglevel_scijava_style, set_verbosity

__version__ = '0.5.3'
