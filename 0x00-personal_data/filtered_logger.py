#!/usr/bin/env python3
"""filtered_logger"""
import logging
import mysql.connector
import os
import re
from typing import List

PII_FIELDS = ('ssn', 'password', 'email', 'phone', 'name')


def filter_datum(fields: List[str],
                 redaction: str,
                 message: str,
                 separator: str) -> str:
    """returns the log message obfuscated"""
    for field in fields:
        pattern = r'({}=)([^{}]+)'.format(field, separator)

        message = re.sub(pattern, r'\1{}'.format(redaction), message)

    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """ Initialize ReactingFormatter"""
        super(RedactingFormatter, self).__init__(self.FORMAT)
        self.fields = fields

    def format(self, record: logging.LogRecord) -> str:
        """Formats the log record"""
        record.msg = filter_datum(
            self.fields,
            self.REDACTION,
            record.getMessage(),
            self.SEPARATOR)

        return super().format(record)


def get_logger() -> logging.Logger:
    """returns a logging.Logger object"""
    user_data = logging.getLogger('user_data')
    user_data.setLevel(logging.INFO)
    user_data.propagate = False

    formatter = RedactingFormatter(PII_FIELDS)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    user_data.addHandler(stream_handler)
    return user_data


def get_db() -> mysql.connector.connection.MySQLConnection:
    """returns a connector to the database"""
    user_name = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = os.getenv('PERSONAL_DATA_DB_NAME', '')

    connection = mysql.connector.connect(
        user=user_name,
        password=password,
        host=host,
        database=db_name)

    return connection


def main():
    """logs the information about user records in a table"""
    fields = 'name,email,phone,ssn,password,ip,last_login,user_agent'
    columns = fields.split(',')
    logger = get_logger()
    conn = get_db()
    query = "SELECT {} from users".format(fields)
    with conn.cursor() as cursor:
        cursor.execute(query)
        rows = cursor.fetchall()
        for row in rows:
            record = map(
                lambda x: '{}={}'.format(
                    x[0], x[1]), zip(
                    columns, row))
            msg = '{};'.format('; '.join(list(record)))
            log_record = logging.LogRecord(
                'user_data', logging.INFO, None, None, msg, None, None)
            logger.handle(log_record)


if __name__ == '__main__':
    main()
