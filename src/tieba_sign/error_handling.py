import logging
import sys
from types import TracebackType
from typing import Callable

import httpx

_original_excepthook = sys.excepthook

def custom_excepthook(exc_type, exc_value, exc_traceback):
    handler: Callable[[type[BaseException], BaseException, TracebackType]]

    match exc_type:
        case httpx.ConnectError:
            handler = excepthook_ConnectError
        case _:
            handler = _original_excepthook

    handler(exc_type, exc_value, exc_traceback)

def excepthook_ConnectError(*_):
    logging.error("无法连接网络")

sys.excepthook = custom_excepthook
