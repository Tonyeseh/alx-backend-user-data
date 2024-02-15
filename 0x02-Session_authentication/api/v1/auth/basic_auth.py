#!/usr/bin/env python3
"""basic_auth module"""

import base64
from typing import TypeVar

from api.v1.auth.auth import Auth
from models.user import User


class BasicAuth(Auth):
    """Basic authentication class"""

    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """returns the Base64 part of the authorization header"""
        if authorization_header and isinstance(authorization_header, str):
            auth_lst = authorization_header.split()
            if len(auth_lst) == 2 and auth_lst[0] == 'Basic':
                return auth_lst[1]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """returns the decoded value of the Base64
        string base64_authorization_header"""
        if base64_authorization_header and isinstance(
                base64_authorization_header, str):
            try:
                auth_str = base64.b64decode(base64_authorization_header)
                return auth_str.decode('utf-8')
            except Exception as e:
                pass

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """returns the user email and password from the base64 decoded value"""
        if decoded_base64_authorization_header and isinstance(
                decoded_base64_authorization_header, str):
            cred = decoded_base64_authorization_header.split(':')
            if len(cred) >= 2:
                return cred[0], ':'.join(cred[1:])
        return (None, None)

    def user_object_from_credentials(
            self,
            user_email: str,
            user_pwd: str) -> TypeVar('User'):
        """returns the User instance based on his email and password"""
        if not user_email or not isinstance(user_email, str):
            return None
        if not user_pwd or not isinstance(user_pwd, str):
            return None

        user = User.search({"email": user_email})
        if user:
            user = user[0]
            if user.is_valid_password(user_pwd):
                return user

    def current_user(self, request=None) -> TypeVar('User'):
        """retrieves the User instance for a request"""
        if request:
            auth_header = self.authorization_header(request)

            if auth_header:
                base64_header = self.extract_base64_authorization_header(
                    auth_header)

                if base64_header:
                    decoded_header = self.decode_base64_authorization_header(
                        base64_header)

                    if decoded_header:
                        credentials = self.extract_user_credentials(
                            decoded_header)
                        print(credentials)
                        if all(credentials):
                            user = self.user_object_from_credentials(
                                *credentials)

                            if user:
                                return user
