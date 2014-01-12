import logging
import sys

DEFAULT_FORMAT = "%(asctime)s %(levelname)8s [%(process)6d %(module)16s.%(funcName)-20s:%(lineno)4d] %(message)s"

def naiveLog(name='default', level='INFO', target='stdout'):
    log = logging.getLogger(name)
    log.setLevel(level)
    if target == 'stdout':
        soutH = logging.StreamHandler(sys.stdout)
    elif target=='stderr':
        soutH = logging.StreamHandler(sys.stderr)
    else:
        raise NotImplementedError
    soutH.setFormatter(logging.Formatter(DEFAULT_FORMAT))
    log.handlers = [soutH]
    return log
