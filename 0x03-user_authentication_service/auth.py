#!/usr/bin/env python3

"""
Authentication module
for ad hoc auth functionalities
"""

from bcrypt import (gensalt, hashpw)


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
