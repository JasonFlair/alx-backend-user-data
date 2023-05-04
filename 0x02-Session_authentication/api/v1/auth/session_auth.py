#!/usr/bin/env python3
"""Session Auth Class created here"""
from typing import Tuple, TypeVar
from .auth import Auth
from uuid import uuid4
from api.v1.views.users import User


class SessionAuth(Auth):
    """Session Authentication class"""
    user_id_by_session_id = {}

    def __init__(self) -> None:
        """Initialiser"""
        super().__init__()

    def create_session(self,
                       user_id: str = None) -> str:
        """Creates a session
        session_id is the key and user_id is the value"""
        if user_id is None:
            return None
        if type(user_id) != str:
            return None
        session_id = str(uuid4())  # convert uuid type to simple string
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self,
                               session_id: str = None) -> str:
        """returns the user_id value of session_id"""
        if session_id is None:
            return None
        if type(session_id) != str:
            return None

        user_id = self.user_id_by_session_id.get(session_id)
        return user_id

    def current_user(self,
                     request=None) -> TypeVar('User'):
        """returns a User instance
        based on a cookie value"""
        session_cookie = self.session_cookie(request)
        user_id = self.user_id_by_session_id.get(session_cookie)
        user = User.get(user_id)
        return user
