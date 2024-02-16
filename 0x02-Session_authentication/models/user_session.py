#!/usr/bin/env python3
""" User Session module
"""

from models.base import Base


class UserSession(Base):
    """ User Session class for sessions"""
    def __init__(self, *args: list, **kwargs: dict):
        """Intialization of the UserSession"""
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
