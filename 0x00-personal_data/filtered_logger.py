#!/usr/bin/env python3
"""filter logger"""

import logging
import os
import re
from typing import List, Tuple

import mysql.connector

PII_FIELDS = ("name", "email", "phone", "ssn", "password")

username = os.getenv("PERSONAL_DATA_DB_USERNAME", "root")
password = os.getenv("PERSONAL_DATA_DB_PASSWORD", "")
db_host = os.getenv("PERSONAL_DATA_DB_HOST", "localhost")
data_base = os.getenv("PERSONAL_DATA_DB_NAME")


def splitter(message: str, separator: str) -> List:
    """splits message for easy iteration"""
    splitted = message.split(separator)
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


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"
    logging.basicConfig(level=logging.INFO, format=FORMAT)

    def __init__(self, fields):
        super(RedactingFormatter, self).__init__(self.FORMAT)
        # call to logging.Formatter, FORMAT is passed to
        # tell logging.Formatter how records will be printed
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """returns a formatted and filtered record
        - implemented call to the format method
          of logging.Formatter, the parent class
        
        - filter_datum performed on the message to censor
        personal details
        
        the censored details is returned
        remember, format() method of logging.Formatter
        is different from format passed to logging.Formatter
        """
        message = super().format(record)
        filtered_record = filter_datum(self.fields,
                                       self.REDACTION,
                                       message,
                                       self.SEPARATOR)
        return filtered_record


def get_logger() -> logging.Logger:
    """gets logger object"""
    this_logger = logging.Logger("user_data", level=logging.INFO)
    this_logger.propagate = False

    # set the streamhandler
    stream_handler = logging.StreamHandler(stream=None)
    # use RedactingFormatter's FORMAT variable as format
    log_format = RedactingFormatter.FORMAT
    stream_handler.setFormatter = log_format
    # add the stream handler as a handler for this logger
    this_logger.addHandler(stream_handler)
    return this_logger


def get_db() -> mysql.connector.connection.MySQLConnection:
    """gets database"""
    return mysql.connector.connect(host=db_host,
                                   database=data_base,
                                   user=username,
                                   password=password)


def main() -> None:
    """main function"""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    for row in cursor:
        print(row[0])
