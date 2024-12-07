from __future__ import annotations

import os
import sys
from functools import lru_cache
from logging import getLogger
from typing import TYPE_CHECKING

from .const import THCC_LOGGER

if TYPE_CHECKING:
    from logging import Logger


PROCESS_ID = os.getpid()


@lru_cache(maxsize=1)
def get_thcc_logger(pid=PROCESS_ID) -> Logger:
    """Returns a THCC specific logger."""

    is_build = hasattr(sys, "frozen")
    DEFAULT_THCC_LOGGER_LEVEL = "DEBUG" if not is_build else "WARNING"

    thcc_logger_level = os.environ.get(
        "THCC_LOGGER_LEVEL", DEFAULT_THCC_LOGGER_LEVEL
    ).upper()
    thcc_logger = getLogger(THCC_LOGGER)
    thcc_logger.setLevel(level=thcc_logger_level)

    return thcc_logger
