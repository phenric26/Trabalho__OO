from flask import Flask, render_template, request, redirect, url_for, flash, session
from app.models.database import init_db
from app.models.product import Product
from app.controllers.user_controller import login_user
from app.controllers.product_controller import *

# Inicializa a aplicação Flask e configura os diretórios de templates e arquivos estáticos
app = Flask(__name__, template_folder=("app/views/templates"), static_folder=("app/views/static"))

# Configuração do banco de dados SQLite
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///estoque.db" 

# Inicializa o banco de dados com a aplicação
init_db(app)

# Rotas da aplicação

# Rota principal que renderiza a página inicial
@app.route("/")
def homepage():
    return render_template("home.html")

# Rota para login, aceita métodos GET e POST
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST": 
        username = request.form["username"]  # Obtém o nome de usuário do formulário
        password = request.form["password"]  # Obtém a senha do formulário
        
        # Verifica as credenciais do usuário
        if login_user(username, password):
            flash("Login bem-sucedido!", "success")
            return redirect(url_for("estoque"))  # Redireciona para a página do estoque
        
        flash("Credenciais inválidas!", "danger")  # Mensagem de erro

    return render_template("login.html")  # Renderiza a página de login

# Rota para exibir a lista de produtos no estoque
@app.route("/estoque")
def estoque():
    return list_products()  # Chama a função que lista os produtos
