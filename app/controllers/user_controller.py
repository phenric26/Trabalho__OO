from flask import request, redirect, url_for, session, flash
from app.models.user import User
from app.models.database import db

# ===================== Função para autenticar um usuário =====================

def login_user(username, password):
    """
    Autentica um usuário no sistema verificando o nome de usuário e a senha.

    Parâmetros:
        username (str): Nome de usuário do usuário tentando fazer login.
        password (str): Senha fornecida pelo usuário.

    Retorno:
        bool: Retorna True se a autenticação for bem-sucedida, False caso contrário.

    Fluxo da função:
        1. Busca um usuário no banco de dados com o nome de usuário fornecido.
        2. Se o usuário existir, verifica se a senha fornecida corresponde à armazenada.
        3. Se a senha estiver correta, a sessão do usuário é criada, armazenando:
            - ID do usuário.
            - Se ele é um administrador.
            - Se ele tem permissões de SuperAdmin.
        4. Retorna True se a autenticação for bem-sucedida, senão retorna False.
    """
    user = User.query.filter_by(username=username).first()  # Busca o usuário pelo nome de usuário

    if user and user.check_password(password):  # Verifica se o usuário existe e a senha está correta
        session['user_id'] = user.id  # Armazena o ID do usuário na sessão
        session['is_admin'] = user.is_admin  # Armazena se o usuário é administrador
        session['is_super_admin'] = user.is_super_admin  # Armazena se o usuário é SuperAdmin
        return True  # Login bem-sucedido
    
    return False  # Retorna False se a autenticação falhar


# ===================== Função para encerrar a sessão do usuário =====================

def logout_user():
    """
    Encerra a sessão do usuário, removendo todas as informações armazenadas.

    Parâmetros:
        Nenhum.

    Retorno:
        Nenhum. Apenas limpa a sessão.

    Fluxo da função:
        1. `session.clear()` remove todos os dados armazenados na sessão.
        2. Isso faz com que o usuário seja deslogado do sistema.
    """
    session.clear()  # Remove todas as informações da sessão, efetivamente deslogando o usuário
