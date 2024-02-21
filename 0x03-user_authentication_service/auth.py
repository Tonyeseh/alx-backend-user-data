#!/usr/bin/env python3
"""auth module"""

from typing import Optional
import uuid
import bcrypt
from sqlalchemy.orm.exc import NoResultFound

from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """takes in a password and returns hash of the password in bytes"""
    salt = bcrypt.gensalt()
    salted_passwd = bcrypt.hashpw(bytes(password, 'utf-8'), salt)

    return salted_passwd


def _generate_uuid() -> str:
    """returns a string representation of a new uuid"""
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a user"""
        try:
            user = self._db.find_user_by(email=email)

            raise ValueError('{} already exists'.format(email))
        except NoResultFound as e:
            pass

        hashed_passwd = _hash_password(password)

        user = self._db.add_user(email, hashed_passwd)

        return user

    def valid_login(self, email: str, password: str) -> bool:
        """return true if credentials are correct else false"""
        try:
            user = self._db.find_user_by(email=email)

            if bcrypt.checkpw(bytes(password, 'utf-8'), user.hashed_password):
                return True

            else:
                return False

        except NoResultFound as e:
            return False

    def create_session(self, email: str) -> str:
        """returns a session ID as string"""
        try:
            user = self._db.find_user_by(email=email)
            sess_id = _generate_uuid()
            self._db.update_user(user.id, session_id=sess_id)

            return sess_id

        except Exception as e:
            return

    def get_user_from_session_id(self, session_id: str) -> Optional[User]:
        """if session_id is None or no user is found, return None.
        Otherwise, return the corresponding user"""
        if session_id is None:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)

            return user

        except Exception as e:
            return None

    def destroy_session(self, user_id: int) -> None:
        """destroy the for the user with user_id"""
        if user_id:
            try:
                self._db.update_user(user_id, session_id=None)

            except ValueError as e:
                return

    def get_reset_password_token(self, email: str) -> str:
        """set and update user reset_token if user exists"""
        try:
            user = self._db.find_user_by(email=email)

            reset_token = _generate_uuid()

            self._db.update_user(user.id, reset_token=reset_token)

            return reset_token

        except Exception as e:
            raise ValueError("Could not find user")

    def update_password(self, reset_token: str, password: str) -> None:
        """user the reset_token to find user and update password"""
        try:
            user = self._db.find_user_by(reset_token=reset_token)

            hashed_password = _hash_password(password)

            self._db.update_user(
                user.id,
                hashed_password=hashed_password,
                reset_token=None)

        except Exception as e:
            raise ValueError("Could not find user")
