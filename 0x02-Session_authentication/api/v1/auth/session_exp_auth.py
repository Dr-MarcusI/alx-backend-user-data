#!/usr/bin/env python3
"""
SessionExpAuth module for the API
"""
from datetime import datetime, timedelta
from os import getenv

from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """A session auth class with expiration to manage the API authentication"""

    def __init__(self):
        """Initialize the session auth from SESSION_DURATION env variable"""
        duration = getenv('SESSION_DURATION')
        self.session_duration = int(
            duration) if duration and duration.isnumeric() else 0

    def create_session(self, user_id: str = None) -> str:
        """Creates a Session ID for a user_id"""
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        self.user_id_by_session_id[session_id] = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Returns a User ID based on a Session ID"""
        if session_id is None:
            return None
        user_session = self.user_id_by_session_id.get(session_id)
        if user_session is None:
            return None
        if self.session_duration <= 0:
            return user_session.get('user_id')
        created_at = user_session.get('created_at')
        if created_at is None:
            return None
        if (created_at +
                timedelta(seconds=self.session_duration)) < datetime.now():
            return None
        return user_session.get('user_id')
