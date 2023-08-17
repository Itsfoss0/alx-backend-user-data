#!/usr/bin/env python3

"""
Test session IDs
"""

from auth import Auth

AUTH = Auth()

print(AUTH._generate_uuid())