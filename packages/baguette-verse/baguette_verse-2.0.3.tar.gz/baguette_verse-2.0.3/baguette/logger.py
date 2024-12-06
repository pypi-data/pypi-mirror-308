"""
This module adds an extensive logging system to the BAGUETTE system.
"""

import logging
import sys

__all__ = ["logger", "stdout_handler", "standart_formatter", "set_level", "get_level", "create_log_file"]





logger = logging.getLogger()
logger.setLevel(0)
stdout_handler = logging.StreamHandler(sys.stdout)
standart_formatter = logging.Formatter("%(levelname)-8s : %(module)-11s : %(asctime)-23s : %(message)s")

logger.addHandler(stdout_handler)
stdout_handler.setFormatter(standart_formatter)





def set_level(level : int):
    """
    Sets the logging level for stdout.
    """
    stdout_handler.setLevel(level)

def get_level() -> int:
    """
    Returns the current logging level for stdout.
    """
    return stdout_handler.level

def create_log_file(path : str, level : int = logging.DEBUG):
    """
    Creates a new log file to which logs with a level higher or equal to the current level will be written.
    """
    handler = logging.FileHandler(path, "w")
    handler.setFormatter(standart_formatter)
    handler.setLevel(level)
    logger.addHandler(handler)

set_level(logging.WARNING)

del logging, sys