#!/usr/bin/env python3
import bcrypt


def hash_password(password: str) -> bytes:
    """returns a salted, hashed password as a byte string"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """returns true if the password is valid, false otherwise"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)
