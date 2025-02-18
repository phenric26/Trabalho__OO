from flask import request, redirect, url_for, session, flash
from app.models.user import User
from app.models.database import db

# Função para autenticar um usuário no sistema
def login_user(username, password):
    user = User.query.filter_by(username=username).first()  # Busca o usuário pelo nome
    if user and user.check_password(password):  # Verifica a senha
        session['user_id'] = user.id  # Armazena o ID do usuário na sessão
        session['is_admin'] = user.is_admin  # Define o status de administrador na sessão
        return True
    return False

# Função para encerrar a sessão do usuário
def logout_user():
    session.clear()  # Remove todas as informações da sessão
