from flask import request, redirect, url_for, session, flash
from app.models.user import User
from app.models.database import db

# Função para autenticar um usuário no sistema
def login_user(username, password):
    user = User.query.filter_by(username=username).first()
    if user and user.check_password(password):
        session['user_id'] = user.id
        session['is_admin'] = user.is_admin
        session['is_super_admin'] = user.is_super_admin  # Adiciona a verificação de SuperAdmin
        return True
    return False




# Função para encerrar a sessão do usuário
def logout_user():
    session.clear()  # Remove todas as informações da sessão
