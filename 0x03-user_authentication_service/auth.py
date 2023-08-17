#!/usr/bin/env python3

"""
Authentication module
for ad hoc auth functionalities
"""

from bcrypt import (gensalt, hashpw)
from sqlalchemy.orm.exc import NoResultFound

from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """
    Hash a password
    Args:
        password (str): the password to hash
    Returns:
        returns the hashed password (bytes)
    =======================================
    Usage:
        password = "mysecurepassword"
        hashed_pwd = _hash_password(password)
        # b'$2b$12$eUDdeuBtrDVH1JbESzgbgZT.eMMzi.G2'
    """
    return hashpw(password.encode(), gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Register a user
        Args:
            email (str): user's email
            password (str): hashed password
            Remember to hash the password
        """
        try:
            existing_user = self._db.find_user_by(email=email)
            # user exists, so we throw an exception
            if existing_user:
                raise ValueError(f'User {email} already exists')
        except NoResultFound:
            # no user with such email
            # so we create a new one
            hashed_password = _hash_password(password)
            return self._db.add_user(email, password)
