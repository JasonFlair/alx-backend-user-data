#!/usr/bin/env python3
"""authentication class created here"""

from typing import List
from flask import request


class Auth:
    """Authentication class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """require auth function"""
        if path is not None:
            if path[-1] != "/":
                path = path + "/"  # include the last slash
        if path is None:
            return True
        if excluded_paths is None or excluded_paths == []:
            return True
        if path not in excluded_paths:
            return True
        elif path in excluded_paths:
            return False

    def authorization_header(self, request=None) -> str:
        """authorization header function"""
        return None

    def current_user(self, request=None) -> str:
        """current user function"""
        return None
