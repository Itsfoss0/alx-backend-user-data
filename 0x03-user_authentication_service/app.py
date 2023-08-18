#!/usr/bin/env python3

"""
Entry point for a simple flask application
"""

from flask import (Flask, jsonify, redirect,
                   request, make_response, abort)
from auth import Auth


AUTH = Auth()
app = Flask(__name__)


@app.route("/", strict_slashes=False, methods=['GET'])
def index():
    """
    entry point
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", strict_slashes=False, methods=["POST"])
def users():
    """
    Handle user auth
    """
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        AUTH.register_user(email, password)
        return jsonify({"email": f"{email}", "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", strict_slashes=False, methods=["POST"])
def sessions():
    """
    Handle session flow
    """
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        if AUTH.valid_login(email, password):
            session_id = AUTH.create_session(email)
            response = make_response(
                {"email": f"{email}",
                    "message": "logged in"}
            )
            response.set_cookie("session_id", session_id)
            return response
        abort(401)
    except Exception:
        abort(401)


@app.route("/sessions", strict_slashes=False, methods=["DELETE"])
def logout():
    """
    Logout the currently logged in user
    """
    session_id = request.cookies.get("session_id")
    current_user = AUTH.get_user_from_session_id(session_id)
    if current_user:
        AUTH.destroy_session(current_user.id)
        return redirect('/')
    abort(403)


@app.route("/profile", strict_slashes=False, methods=["GET"])
def profile():
    """
    User's profile
    """
    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)
    if user:
        return jsonify({"email": f"{user.email}"})
    abort(403)


@app.route("/password_reset", strict_slashes=False, methods=["POST"])
def get_reset_password_token():
    """
    POST /password_reset
    to reset user's password
    """
    email = request.form.get('email')
    if email:
        try:
            r_token = AUTH.get_reset_password_token(email)
            return jsonify({
                "email": f"{email}",
                "reset_token": f"{r_token}"}
            ), 200
        except ValueError:
            abort(403)
    abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
