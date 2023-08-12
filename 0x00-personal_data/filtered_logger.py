#!/usr/bin/env python3

"""
This module contains the functions
to filter  personal data from logs
and obfuscate it for log processing
"""

PII_FIELDS = ("name", "email", "ssn", "password", "phone")


import logging  # noqa E402
import re  # noqa E402
from typing import List  # noqa E402
from mysql.connector.connection import MySQLConnection  # noqa E402
from os import environ  # noqa E402


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
    # if not isinstance(fields, list) or not isinstance(redaction, str)\
    #     or not isinstance(message, str) or not isinstance(separator, str):
    #     raise TypeError('Check your arguments')

    for field in fields:
        message = re.sub(f'{field}=.*?{separator}',
                     f'{field}={redaction}{separator}', message)  # noqa E128
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """
        The constructor for the RedactingFormatter
        Args:
            fields (list): A list of fields to redact
        """
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """
        Format a log message by removing the PIII
        Args:
            record (logRecord): The log record to format
        Returns:
            returns a string
        """
        record.msg = filter_datum(self.fields, RedactingFormatter.REDACTION,
                        record.getMessage(), RedactingFormatter.SEPARATOR)  # noqa E128
        return super(RedactingFormatter, self).format(record)


def get_logger() -> logging.Logger:
    """
    This function returns a Logger object
    Args:
        doesn't take any arguments
    Returns:
        returns a Logger
    """
    holbie_logger = logging.getLogger("user_data")
    holbie_logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter(PII_FIELDS))
    holbie_logger.propagate = False
    return holbie_logger


def get_db() -> MySQLConnection:
    """
    connect to a database securely using
    mysql.connector
    ------------------------------------
    Example:
        db_obj = get_db()
        db_objet.cursor().execute(query)
    """
    DB_CREDS_STUB = {
        "username": environ.get("PERSONAL_DATA_DB_USERNAME", "root"),
        "password": environ.get("PERSONAL_DATA_DB_PASSWORD", "root"),
        "database": environ.get("PERSONAL_DATA_DB_NAME", "my_db"),
        "host": environ.get("PERSONAL_DATA_DB_HOST", "localhost")
    }
    return MySQLConnection(**DB_CREDS_STUB)


def main():
    """
    Entry point for the script
    Fetches users from the database and logs
    the records with PII stripped
    """
    logger = get_logger()
    connection = get_db()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM users")
    fields = [entry[0] for entry in cursor.description]
    # return cursor.fetchall()
    for row in cursor:
        record_wit_fields = "".join(f"{i} {str(j)}" for i, j in zip(row, fields)).strip()
        logger.info(record_wit_fields)
    # return fields


if __name__ == "__main__":
    print(main())
