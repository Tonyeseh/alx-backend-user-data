#!/usr/bin/env python3
"""session_db_auth module"""

from datetime import datetime, timedelta
import uuid
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """Session DB Auth class"""

    def create_session(self, user_id=None):
        """Creates and stores new instance of UserSession and
        return the Session ID"""
        if user_id is None:
            return None

        session_id = str(uuid.uuid4())
        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()
        print(user_session.to_json())
        return user_session.session_id
        
    def user_id_for_session_id(self, session_id=None):
        """returns the User Id by requesting UserSession in the database on session_id"""
        if session_id is None:
            return None
        
        user_session = UserSession.search({"session_id": session_id})

        if not user_session:
            return None
        
        user_session = user_session[0]

        if self.session_duration <= 0:
            return user_session.user_id
        
        time_exp = user_session.created_at + timedelta(seconds=self.session_duration)

        if time_exp < datetime.now():
            return None

        return user_session.user_id
    
    def destroy_session(self, request=None):
        """Destroys the UserSession based on the Session ID from the request cookie."""
        if request is None:
            return False
        
        sess_cookie = self.session_cookie(request)

        if not sess_cookie:
            return False
        
        user_session = UserSession.get({"session_id": sess_cookie})

        if not user_session:
            return False
        print(user_session)
        user_session = user_session[0]

        user_session.remove()

        return True
