#!/usr/bin/env python3
"""session_auth module"""

import uuid
from api.v1.auth.auth import Auth

class SessionAuth(Auth):
    """Session authentication class"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """creates a new Session ID for a user_id"""
        if not user_id or isinstance(user_id, str):
            return None
        
        new_sess_id = str(uuid.uuid4())
        self.user_id_by_session_id[new_sess_id] = user_id

        return new_sess_id
