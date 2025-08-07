from flask import Blueprint, request, jsonify
from .models import User
from . import db
import requests


user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    if User.query.filter_by(username=data['username']).first():
        return jsonify({"message": "Username already exists"}), 400

    user = User(username=data['username'], email=data['email'])
    user.set_password(data['password'])
    db.session.add(user)
    db.session.commit()

    # 🔔 Send notification
    try:
        requests.post("http://notification-service:5053/notify", json={
            "type": "registration",
            "user": user.username,
            "email": user.email
        })
    except Exception as e:
        print("Failed to send notification:", e)

    return jsonify({"message": "User registered"}), 201

@user_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data['username']).first()
    if user and user.check_password(data['password']):
        return jsonify({"message": "Login successful"})
    return jsonify({"message": "Invalid credentials"}), 401

@user_bp.route('/profile/<username>', methods=['GET'])
def profile(username):
    user = User.query.filter_by(username=username).first()
    if user:
        return jsonify({
            "username": user.username,
            "email": user.email
        })
    return jsonify({"message": "User not found"}), 404
