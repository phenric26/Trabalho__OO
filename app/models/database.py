from flask_sqlalchemy import SQLAlchemy

# Criação da instância global do banco de dados
db = SQLAlchemy()

def init_db(app):
    """
    Inicializa o banco de dados com a aplicação Flask.

    Parâmetros:
        app (Flask): Instância da aplicação Flask.

    Funcionalidade:
        - Associa a instância do banco de dados `db` à aplicação Flask.
        - Cria todas as tabelas definidas nos modelos se ainda não existirem.
        - Garante que as operações com o banco sejam realizadas dentro do contexto da aplicação.
    """
    db.init_app(app)  # Configura a aplicação para utilizar SQLAlchemy

    with app.app_context():  
        # Cria as tabelas no banco de dados (caso ainda não existam)
        db.create_all()  
