#!/usr/bin/env python3
"""filter logger"""

import re
from typing import List, Tuple


def splitter(message: str, separator: str) -> List:
    """splits message for easy iteration"""
    splitted = message.split(";")
    return splitted


def pattern_rplc(field, redaction) -> Tuple:
    """sets pattern and replacement to
    be used with re.sub"""
    pattern = field + ".*"
    replacement = field + "=" + redaction
    return pattern, replacement


def filter_datum(fields: List[str],
                 redaction: str,
                 message: str,
                 separator: str) -> str:
    """returns the log message obfuscated
    with personal data protected"""
    new_list = splitter(message, separator)
    for field in fields:
        pattern, replacement = pattern_rplc(field, redaction)
        for idx, val in enumerate(new_list):
            new_list[idx] = re.sub(pattern, replacement, val)
    return ";".join(new_list)
