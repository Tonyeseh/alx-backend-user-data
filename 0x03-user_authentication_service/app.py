#!/usr/bin/env python3
"""app module"""

from flask import abort, Flask, jsonify, redirect, request

from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route('/', methods=['GET'])
def index():
    """Return a welcome message in french(json)"""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def users():
    """registers a new user"""
    try:
        rj = request.form
        print(request.get_json())
        print(rj)
        if rj.get('email', None) is None:
            raise ValueError("No email address")
        if rj.get('password', None) is None:
            raise ValueError("No password")

        try:
            user = AUTH.register_user(rj.get('email'), rj.get('password'))

            if user:
                return jsonify(
                    {"email": user.email, "message": "user created"})

        except ValueError:
            return jsonify({"message": "email already registered"})

    except Exception as err:
        print(err)
        return jsonify({"message": "Invalid payload"}), 400


@app.route('/sessions', methods=['POST'])
def login():
    """check for sessions and create if not found"""
    rf = request.form

    if not rf:
        return jsonify({"message": "Invalid payload"}), 400

    if not rf.get('email'):
        return jsonify({"message": "No email provided"}), 400

    if not rf.get('password'):
        return jsonify({"message": "No password provided"}), 400

    authorized = AUTH.valid_login(rf.get('email'), rf.get('password'))

    if not authorized:
        abort(401)

    sess_id = AUTH.create_session(rf.get('email'))

    if not sess_id:
        return jsonify({"message": "Could not login"}), 403

    resp = jsonify({"email": rf.get('email'), "message": "logged in"})

    resp.set_cookie('session_id', sess_id)

    return resp


@app.route('/sessions', methods=['DELETE'])
def logout():
    """destroy session if user exists, otherwise respone with 403 status"""
    session_id = request.cookies.get('session_id')

    if session_id:
        user = AUTH.get_user_from_session_id(session_id)

        if user:
            AUTH.destroy_session(user.id)
            redirect('/')

    abort(403)


@app.route('/profile', methods=['GET'])
def profile():
    """returns user profile if user exists"""
    session_id = request.cookies.get('session_id')

    if session_id:
        user = AUTH.get_user_from_session_id(session_id)

        if user:
            return jsonify({"email": user.email})

    abort(403)


@app.route('/reset_password', methods=['POST'])
def get_reset_password_token():
    """if email is not registered return 403 status.
    Otherwise, get retoken and return"""
    email = request.form.get('email')

    if email:
        try:
            token = AUTH.get_reset_password_token(email)

            return jsonify({"email": email, "token": token})

        except ValueError:
            pass

    abort(403)


@app.route('/reset_password', methods=['PUT'])
def update_password():
    """Update user password"""
    rf = request.form

    email = rf.get('email')
    reset_token = rf.get('reset_token')
    new_password = rf.get('new_password')

    if all(new_password, email, reset_token):
        try:
            AUTH.update_password(reset_token, new_password)

            return jsonify({"email": email, "message": "Password updated"})

        except Exception as e:
            pass


if __name__ == '__main__':
    app.run(host='0.0.0.0', port='5000', debug=True)
