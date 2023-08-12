#!/usr/bin/env python3

"""
hash passwords using bcrypt
"""

from bcrypt import hashpw, gensalt


def hash_password(pwd: str) -> bytes:
    """
    Hash a password
    Args:
        pwd (str): the password to hash
    Returns:
        returns a bytestring of the hashed pwd
    Exceptions:
        Raises TypeError if the pwd is not of type str
    ------------------------------------------------
    Example:
        hash_password("MyAmazingPassw0rd")
        # b'$2b$12$Fnjf6ew.oPZtVksngJjh1.vYCnxRjPm2yt18kw6AuprMRpmhJVxJO'
        hash_password(1234)
        # TypeError 1234 is not of type str
    """
    try:
        if isinstance(pwd, str):
            return hashpw(pwd.encode("utf-8"), gensalt())

        raise TypeError(f"{pwd} is not of type str")
    except Exception as e:
        return e.__context__
