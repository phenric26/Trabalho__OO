from flask import request, redirect, url_for, session, flash
from app.models.user import User
from app.models.database import db

def login_user(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        session['user_id'] = user.id
        session['is_admin'] = user.is_admin
        return True
    return False

def logout_user():
    session.clear()
