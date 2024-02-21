#!/usr/bin/env python3
"""Main module"""

import requests

route = 'http://localhost:5000/'


def register_user(email: str, password: str) -> None:
    """tests the register route of application"""
    response = requests.post(
        route + 'users',
        data={
            'email': email,
            'password': password})

    response2 = requests.post(
        route + 'users',
        data={
            'email': email,
            'password': password})

    assert response.json() == {'email': email, "message": "user created"}
    assert response.status_code == 200

    assert response2.json() == {"message": "email already registered"}
    assert response2.status_code == 400


def log_in_wrong_password(email: str, password: str) -> None:
    """test with wrong login credentials"""
    respose = requests.post(
        route + 'sessions',
        data={
            'email': email,
            'password': password})

    assert respose.status_code == 401


def log_in(email: str, password: str) -> str:
    """test with correction login credentials"""
    response = requests.post(
        route + 'sessions',
        data={
            'email': email,
            'password': password})

    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "logged in"}

    return response.cookies['session_id']


def profile_unlogged() -> None:
    """test for profile request without session_id"""
    response = requests.get(route + 'profile',)

    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """test for profile request with session id"""
    response = requests.get(
        route + 'profile',
        cookies={
            "session_id": session_id})

    assert response.status_code == 200
    assert response.json() == {"email": EMAIL}


def log_out(session_id: str) -> None:
    """test for logout route with session id"""
    response = requests.delete(
        route + 'sessions',
        cookies={
            "session_id": session_id})

    assert response.status_code == 200


def reset_password_token(email: str) -> str:
    """reset password with token route"""
    response = requests.post(route + 'reset_password', data={"email": email})

    assert response.status_code == 200
    assert response.json().get("email") == email
    assert 'reset_token' in response.json().keys()

    return response.json().get('reset_token')


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """update password route"""
    response = requests.put(
        route + 'reset_password',
        data={
            "email": email,
            "reset_token": reset_token,
            "new_password": new_password})

    assert response.status_code == 200
    assert response.json() == {"email": email, "message": "Password updated"}


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"

if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
