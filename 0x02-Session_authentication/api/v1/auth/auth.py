#!/usr/bin/env python3

"""
This module hold the auth class
to handle API authentication in our
API system
"""

from flask import request
from typing import TypeVar, List


class Auth:
    """
    A simple  auth class to handle
    API authentication
    """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        check if the  endpoint requires authentication
        Args:
            path (str):  endpoint to check
            excluded_paths(list): a list of paths
        Returns:
            returns a boolean
        -------------------------------------------
        Example:
            auth = Auth()
            auth.require_auth("/api/private", []) # True
            auth.require_auth("/api/public", []) # False
        """
        if path is None:
            return True

        if excluded_paths is None or not excluded_paths:
            return True

        slash_path = path if path.endswith('/') else path + '/'
        excluded_paths_with_slash = [p if p.endswith('/')
                                     else p + '/' for p in excluded_paths]

        return slash_path not in excluded_paths_with_slash

    def authorization_header(self, request=None) -> str:
        """
        Get the authorization header from a http request
        Args:
            requests (dict): A reqeust object
        Returns:
            returns the Authorization header from
            a http request
        """
        if request and request.headers.get("Authorization"):
            return request.headers.get("Authorization")
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Get the current user
        Args:
            request (object): A HTTP request
        Returns:
            returns the current user
        """
        return None
