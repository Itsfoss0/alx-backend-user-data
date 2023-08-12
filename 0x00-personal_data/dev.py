#!/usr/bin/env python3

"""
connect to a database securely
using a custom context manager
"""

import mysql.connector as connector
from os import getenv


credentials = {
    "username": getenv(PERSONAL_DATA_DB_USERNAME, "root"),
    "password": getenv(PERSONAL_DATA_DB_PASSWORD, "root"),
    "database": getenv(PERSONAL_DATA_DB_NAME, "my_db"),
    "host": getenv(PERSONAL_DATA_DB_HOST, "localhost")
}
# using a context manager instead


class ConnectDatabase:

    """
    connect to mysql database
    """

    def __init__(self, creds):
        """
        the constructor to initialize the database
        connection  and return the connection object
        """
        self.connection = connector.Connect(**creds)

    def __enter__(self):
        """
        The enter state for our context manager
        Returns the conection object
        Args:
            None
        """
        return self.connection

    def __exit__(self, *args):
        """
        Gracefully shutdown the connection
        And tear down the resources
        """
        self.connection.close()


# with ConnectDatabase(credentials) as db:
#     cursor = db.cursor()
#     cursor.execute("SELECT * FROM users")
#     print(cursor.fetchall())
