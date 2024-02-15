#!/usr/bin/env python3
"""session_exp_auth module"""
import os
from datetime import datetime, timedelta

from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """Session Exp Authorization class"""

    def __init__(self):
        """Initialize the session"""
        try:
            session_duration = os.getenv('SESSION_DURATION', 0)
            self.session_duration = int(session_duration)

        except Exception as e:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """Create a session ID"""
        sess_id = super().create_session(user_id)

        if not sess_id:
            return None

        self.user_id_by_session_id[sess_id] = {
            "user_id": user_id,
            "created_at": datetime.now()
        }

        return sess_id

    def user_id_for_session_id(self, session_id=None):
        """return a user ID based on session ID"""
        if session_id is None:
            return None

        session_dict = self.user_id_by_session_id.get(session_id)

        if session_dict is None:
            return None

        if self.session_duration <= 0:
            return session_dict.get('user_id')

        if not session_dict.get('created_at'):
            return None

        time_exp = (
            session_dict.get('created_at') +
            timedelta(
                seconds=self.session_duration))

        if time_exp < datetime.now():

            return None

        return session_dict.get('user_id')
