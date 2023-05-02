#!/usr/bin/env python3
"""basic authentication class created here"""
from typing import Tuple, TypeVar
from .auth import Auth
import base64


class BasicAuth(Auth):
    """Basic Auth class"""

    def __init__(self) -> None:
        """initialiser"""
        super().__init__()

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """base64 authorization header"""
        if authorization_header is None:
            return None
        if type(authorization_header) != str:
            return None

        if authorization_header[:6] != "Basic ":
            return None

        return authorization_header[6:]

    def decode_base64_authorization_header(self,
                                           base64_authorization_header:
                                               str) -> str:
        """decodes base64 authorization header"""
        if base64_authorization_header is None:
            return None
        if type(base64_authorization_header) != str:
            return None

        try:
            encoded_data = base64.b64decode(base64_authorization_header)
            return encoded_data.decode("utf-8")
        except Exception:
            return None

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header:
                                     str) -> Tuple[str, str]:
        """returns the user email and password
        from the Base64 decoded value."""
        if decoded_base64_authorization_header is None:
            return None, None

        if type(decoded_base64_authorization_header) != str:
            return None, None

        if ":" not in decoded_base64_authorization_header:
            return None, None

        email_password = decoded_base64_authorization_header.split(":")
        return email_password[0], email_password[1]
    
    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """returns the User instance
        based on his email and password."""
        