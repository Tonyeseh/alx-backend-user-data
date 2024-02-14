#!/usr/bin/env python3
"""auth module"""
from typing import List, TypeVar


class Auth:
    """A simple authentication class """

    def require_auth(self, path: str, exclude_paths: List[str]) -> bool:
        """returns True if the path is not in
        the list of strings exclude_paths"""
        if not path or not exclude_paths:
            return True

        if not path.endswith('/'):
            path = path + '/'

        for p in exclude_paths:
            if p.endswith('*'):
                p = p[:-1]
                if p in path:
                    return False
            else:
                if p == path:
                    return False

        return True

    def authorization_header(self, request=None) -> str:
        """returns the value in the Authorization header of the request"""
        if not request:
            return None

        auth_header = request.headers.get('Authorization')

        if auth_header is None:
            return None

        return auth_header

    def current_user(self, request=None) -> TypeVar('User'):
        """returns None for now"""
        return None
