#!/usr/bin/env python3
""" Module of Session Auth views
"""
from flask import abort, jsonify, request

from api.v1.views import app_views
from models.user import User


@app_views.route('/auth_session/login/',
                 methods=['POST'], strict_slashes=False)
def auth_session_login():
    """Session Authentication Route"""
    email = request.form.get('email')
    password = request.form.get('password')

    if not email:
        return jsonify({"error": "email missing"}), 400

    if not password:
        return jsonify({"error": "password missing"}), 400

    user = User.search({"email": email})
    if not user:
        return jsonify({"error": "no user found for this email"}), 404

    user = user[0]

    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth

    session_id = auth.create_session(user.id)

    resp = jsonify(user.to_json())
    resp.set_cookie('_my_session_id', session_id)

    return resp


@app_views.route('/auth_session/logout/',
                 methods=['DELETE'],
                 strict_slashes=False)
def session_logout():
    """delete session route"""
    from api.v1.app import auth

    if auth.destroy_session(request):
        return jsonify({})

    abort(404)
