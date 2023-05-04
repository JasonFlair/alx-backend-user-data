#!/usr/bin/env python3
""" Module of Session Auth views
"""
from api.v1.views import app_views
from flask import abort, jsonify, make_response, request
from models.user import User


@app_views.route("/auth_session/login",
                 methods=['POST'], strict_slashes=False)
def session_auth_route(request):
    """session auth route"""
    email = request.form.get("email")
    password = request.form.get("password")
    if email is None:
        return make_response(jsonify({"error": "email missing"}), 400)
    if password is None:
        return make_response(jsonify({"error": "password missing"}), 400)
    user = User.search({"email": email})