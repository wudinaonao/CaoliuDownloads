import os
import sys

sys.path.append(os.path.split(os.path.dirname(os.path.abspath(__file__)))[0])

import colorlog
import logging
import os
from Config.Config import LEVEL
from Config.Config import LOG_FILE


class Log():
    # read configure get user set log level
    _LEVEL = LEVEL
    _LEVEL_ENUM = {
        "GENERAL": 0,
        "DETAILED": 1,
        "ALL": 2
    }
    
    _logger = colorlog.getLogger()
    _logger.setLevel(logging.INFO)
    
    # screen output color log
    _ch = colorlog.StreamHandler()
    _screenFormatter = colorlog.ColoredFormatter(
        "%(log_color)s[%(asctime)s] %(log_color)s%(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        reset=True,
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'cyan,bg_white',
        },
        secondary_log_colors={},
        style='%'
    )
    _ch.setFormatter(_screenFormatter)
    
    # file output normal log
    _logPath = os.path.join(os.path.split(os.path.dirname(os.path.abspath(__file__)))[0], LOG_FILE)
    _fh = logging.FileHandler(_logPath, encoding='utf-8')
    _fileLogFormatter = logging.Formatter("[%(asctime)s] %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    _fh.setFormatter(_fileLogFormatter)
    
    _logger.addHandler(_ch)
    _logger.addHandler(_fh)
    
    @classmethod
    def info(cls, string, level="GENERAL"):
        if cls._LEVEL_ENUM[cls._LEVEL] >= cls._LEVEL_ENUM[level]:
            cls._logger.info(string)
    
    @classmethod
    def error(cls, string, level="GENERAL"):
        if cls._LEVEL_ENUM[cls._LEVEL] >= cls._LEVEL_ENUM[level]:
            cls._logger.error(string)
    
    @classmethod
    def warning(cls, string, level="GENERAL"):
        if cls._LEVEL_ENUM[cls._LEVEL] >= cls._LEVEL_ENUM[level]:
            cls._logger.warning(string)
    
    @classmethod
    def critical(cls, string, level="GENERAL"):
        if cls._LEVEL_ENUM[cls._LEVEL] >= cls._LEVEL_ENUM[level]:
            cls._logger.critical(string)
    
    @classmethod
    def debug(cls, string, level="GENERAL"):
        if cls._LEVEL_ENUM[cls._LEVEL] >= cls._LEVEL_ENUM[level]:
            cls._logger.debug(string)


if __name__ == '__main__':
    logger = Log
    logger.info("info")
    logger.error("error", level="DETAILED")
    logger.warning("warning", level="ALL")


