#!/usr/bin/env python3
"""session_auth module"""

from typing import TypeVar
import uuid
from api.v1.auth.auth import Auth
from models.user import User


class SessionAuth(Auth):
    """Session authentication class"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """creates a new Session ID for a user_id"""
        if not user_id or not isinstance(user_id, str):
            return None

        new_sess_id = str(uuid.uuid4())
        self.user_id_by_session_id[new_sess_id] = user_id

        return new_sess_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """return a user ID based on session ID"""
        if session_id is None and not isinstance(session_id, str):
            return None
        return self.user_id_by_session_id.get(session_id, None)

    def current_user(self, request=None) -> TypeVar('User'):
        """returns the current user from the session"""
        sess_cookie = self.session_cookie(request)

        if sess_cookie:
            user_id = self.user_id_for_session_id(sess_cookie)

            return User.get(user_id)

    def destroy_session(self, request=None):
        """deletes the user session/logout"""
        if request is None:
            return False

        sess_cookie = self.session_cookie(request)

        if not sess_cookie:
            return False

        user_id = self.user_id_for_session_id(sess_cookie)

        if not user_id:
            return False

        try:
            del self.user_id_by_session_id[sess_cookie]

        except Exception as e:
            pass

        return True
