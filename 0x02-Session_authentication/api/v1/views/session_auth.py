#!/usr/bin/env python3
""" Module of Session Auth views
"""
import os
from typing import Dict
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models.user import User


@app_views.route("/auth_session/login",
                 methods=['POST'], strict_slashes=False)
def session_auth_route() -> Dict:
    """session auth route"""
    email = request.form.get("email")
    password = request.form.get("password")
    if email is None:
        return make_response(jsonify({"error": "email missing"}), 400)
    if password is None:
        return make_response(jsonify({"error": "password missing"}), 400)
    users = User.search({"email": email})
    if users is None:
        return make_response(jsonify({"error":
                                      "no user found for this email"}), 404)
    else:
        from api.v1.app import auth
        for user in users:
            password_validity = user.is_valid_password(password)
            if password_validity is False:
                return make_response(jsonify({"error": "wrong password"}), 401)
            session_created = auth.create_session(user.id)
            SESSION_NAME = os.getenv("SESSION_NAME")
            """from stackoverflow:
            jsonify returns a Response object,
            so capture it before returning from your view
            and add the cookie then with Response.set_cookie"""
            user_response = jsonify(user.to_json())
            user_response.set_cookie(SESSION_NAME, session_created)
            # return the user response which is the user json and
            # the cookie set
            return user_response


@app_views.route('/auth_session/logout', methods=['DELETE'],
                 strict_slashes=False)
def handle_logout():
    """
    Handle user logout
    """
    from api.v1.app import auth
    if auth.destroy_session(request):
        return jsonify({}), 200
    abort(404)
