#!/usr/bin/env python3

"""
Basic Auth
this module provides the basic auth class
for HTTP authorization
"""

from .auth import Auth
from base64 import b64decode
import re
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """
    Basic Auth class
    for Basic HTTP authorization
    """
    @staticmethod
    def is_valid_basic_header(auth_header: str) -> str:
        """
        A simple function to validate headers
        Args:
            auth_header (str): string to validate against
        Returns:
            returns a boolean
        Example
            is_valid_header("Basic aXRzZm9zczppdHNmb3NzCg==")
            # True
            is_valid_header("Not a valid input")
            # False
        """
        pattern = r'^Basic [a-zA-Z0-9\-]*'
        return re.match(pattern, auth_header) is not None

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """
        extract the base64  from the header
        Args:
            authorization_header(str): the header in reference
        Returns:
            returns a string (base64)
        """
        if not authorization_header or not\
                isinstance(authorization_header, str):
            return None
        if not BasicAuth.is_valid_basic_header(authorization_header):
            return None
        return authorization_header.split(" ")[1]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header:
                                           str) -> str:
        """
        decode the base64 string after extracting it
        Args:
            base64_authorization_header(str): string to decode
        Returns:
            returns a utf-8 string
        """
        if not base64_authorization_header or not isinstance(
                    base64_authorization_header, str):
            return None
        try:
            return (b64decode(base64_authorization_header).decode('utf-8'))
        except Exception as e:
            return None

    def extract_user_credentials(self, decoded_header: str) -> (str, str):
        """
        extract user credentials from the decode string
        Args:
            decoded_header (str): the decoded base64
        Returns:
            returns a tuple (str, str)
        -----------------------------------------------
        Example:
            auth = BasicAuth()
            creds: str = auth.extract_user_credentials("john: doe")
            # ('john', 'doe')
        """
        if not decoded_header or not isinstance(decoded_header, str):
            return (None, None)
        last_colon_index = decoded_header.rfind(":")
        if last_colon_index != -1:
            username = decoded_header[:last_colon_index]
            password = decoded_header[last_colon_index + 1:]
            return (username, password)
        return (None, None)

    def user_object_from_credentials(
        self,
        user_email: str,
            user_pwd: str) -> TypeVar('User'):
        """
        get the user object from the credentials
        Args:
            user_email (str): the username
            user_pwd  (str): the password
        Returns:
            returns a object  of the User class
        """
        if not user_email or not user_pwd or not isinstance(user_email, str)\
                or not isinstance(user_pwd, str):
            return None
        try:
            users = User.search({"email": user_email})
            if not users or users == []:
                return None
            for user in users:
                if user.is_valid_password(user_pwd):
                    return user
        except Exception as e:
            return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Get the current user
        Args:
            request (str): The HTTP request in question
        Returns:
            returns a user object
        """
        auth_header = self.authorization_header(request)
        if auth_header is not None:
            token = self.extract_base64_authorization_header(auth_header)
            if token is not None:
                decoded = self.decode_base64_authorization_header(token)
                if decoded is not None:
                    email, password = self.extract_user_credentials(decoded)
                    if email is not None:
                        return self.user_object_from_credentials(
                            email, password)

        return
