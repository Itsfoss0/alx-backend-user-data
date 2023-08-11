#!/usr/bin/env python3

"""
This module contains the functions
to filter  personal data from logs
and obfuscate it for log processing
"""

from re import sub
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    """
    A simple function to filter some field from
    a message, given the seperator
    Args:
        fields (list):  a list of fields to filter
        redaction (str): What to replace the fileds with
        message (str): the message to obfuscate
        seperator (str):  the message seperator
    Returns:
        returns a string
    -----------------------------------------------
    Example:
        message = "name=egg;email=eggmin@eggsample.com;pwd=eggcellent"
        filtered = filter_datum(["email", "pwd"], "***", message, ";")
        # should return "name=egg;email=***;pwd=***
    Exceptions:
        raises TypeError if the args are not of the valid type
    """
    if not isinstance(fields, list) or not isinstance(redaction, str)\
            or not isinstance(message, str) or not isinstance(separator, str):
        raise TypeError('Check your arguments')

    for field in fields:
        message = sub(f'{field}=.*?{separator}',
                     f'{field}={redaction}{separator}', message)  # noqa E128
    return message
