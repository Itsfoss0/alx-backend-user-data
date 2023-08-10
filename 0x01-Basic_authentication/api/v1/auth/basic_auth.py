#!/usr/bin/env python3

"""
Basic Auth
this module provides the basic auth class
for HTTP authorization
"""

from .auth import Auth
from base64 import b64decode
import re


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
        if ":" in decoded_header:
            return tuple(decoded_header.split(":"))
        return (None, None)
