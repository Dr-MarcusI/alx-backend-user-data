#!/usr/bin/env python3
"""
Auth module for the API
"""
import re
from os import getenv
from typing import List, TypeVar

from flask import request


class Auth:
    """A class to manage the API authentication"""

    def require_auth(self, path: str, exclude_paths: List[str]) -> bool:
        """
        Require authentication for all the paths except the ones in
        exclude_paths

        Return:
            - True if the path is not in the list of strings exclude_paths
            else False
        """
        if path is None or exclude_paths is None or exclude_paths == []:
            return True
        path = path + '/' if path[-1] != '/' else path
        for exclude_path in exclude_paths:
            exclude_path = exclude_path.replace('/', '\\/').replace('*', '.*')
            regex = re.compile(exclude_path)
            if regex.search(path):
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Return:
            - the value of the header request Authorization or None
            if request doesn't contain Authorization header
        """
        if request is None:
            return None
        return request.headers.get('Authorization', None)

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Return:
            - the current user
        """
        return None

    def session_cookie(self, request=None):
        """
        Return:
            - the value of the cookie request.session_id or None
        """
        if request is None:
            return None
        return request.cookies.get(getenv('SESSION_NAME'))
