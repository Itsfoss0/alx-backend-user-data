#!/usr/bin/env python3

"""
Authentication module
for ad hoc auth functionalities
"""

from bcrypt import (gensalt, hashpw, checkpw)
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4

from db import DB
from user import User


def _generate_uuid() -> str:
    """
    Genereate Universally Unique IDs
    to represent sessions
    Usage:
        _generate_uuid()
        # 2a633dcf-a832-4ff9-87b3-75666c4744a5
    """
    return str(uuid4())


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
            return self._db.add_user(email, hashed_password)

    def valid_login(self, email: str, password: str) -> bool:
        """
        validate user credentials agains those in the DB
        Args:
            email (str):  login email
            passowrd (str): login password
        """
        try:
            login_user = self._db.find_user_by(email=email)
            return checkpw(password.encode(), login_user.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email):
        """
        Create a user session
        Args:
            email (str): user's email
        Returns:
            returns a string (session id)
        _________________________________
        Example Usage:
            from auth import Auth
            auth = Auth()

            email = "john@doe.net"
            auth.create_session(email)
            # 5a006849-343e-4a48-ba4e-bbd523fcca58
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> User:
        """
        Get a user from the session ID
        Args:
            session_id (str): user's session ID
        Returns:
            returns a user (object of User)
        """
        if not session_id:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        Destory a user's session
        Args:
            user_id (int): user's ID
        Returns:
            returs None (explicity)
        """
        new_session = {
            "session_id": None
        }
        user = self._db.update_user(user_id, **new_session)

    def get_reset_password_token(self, email: str) -> str:
        """
        Generate a password reset token for the user
        Args:
            email (str): user's email
        Returns:
            returns a string
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                token = _generate_uuid()
                self._db.update_user(user.id, reset_token=token)
                return token
            raise ValueError('User not found!')
        except NoResultFound:
            raise ValueError
