from flask import Flask, render_template, request, redirect, url_for, flash, session
from app.models.database import init_db
from app.models.product import Product
from app.controllers.user_controller import *
from app.controllers.product_controller import *
import os
# Inicializa a aplicação Flask e configura os diretórios de templates e arquivos estáticos
app = Flask(__name__, template_folder=("app/views/templates"), static_folder=("app/views/static"))
app.secret_key = os.getenv('SECRET_KEY', 'sua_chave_secreta')

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

@app.route("/cadastro", methods=["GET", "POST"])
def cadastrar():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        admin = 'admin' in request.form  # Verifica se a opção admin foi marcada

        # Verifica se o usuário já existe no banco de dados
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Erro: Nome de usuário já está em uso.", "danger")
            return redirect(url_for('cadastro'))  # Redireciona para a página de cadastro

        # Se o nome de usuário for único, cria um novo usuário
        new_user = User(username=username, is_admin=admin)
        new_user.set_password(password)  # Método para armazenar a senha de forma segura
        db.session.add(new_user)
        db.session.commit()

        flash("Usuário cadastrado com sucesso!", "success")
        return redirect(url_for("estoque"))  # Redireciona após cadastro bem-sucedido

    return render_template("cadastro.html")


@app.route("/logout")
def logout():
    logout_user()  # Limpa as informações da sessão
    flash("Você saiu com sucesso.", "success")  # Exibe mensagem de sucesso
    return redirect(url_for("homepage"))

# Rota para exibir a lista de produtos no estoque
@app.route("/estoque")
def estoque():
    return list_products()  # Chama a função que lista os produtos

@app.route('/add_product', methods=['GET', 'POST'])
def add_product_route():
    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']
        price = request.form['price']
        add_product(name, quantity, price)  # Chama a função add_product para adicionar o produto
        flash("Produto adicionado com sucesso!", "success")
        return redirect(url_for('estoque'))  # Redireciona para a página de estoque
    return render_template('add_product.html')  # Página de formulário para adicionar produto

@app.route('/update_product/<int:product_id>', methods=['GET', 'POST'])
def update_product_route(product_id):
    product = Product.query.get(product_id)
    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']
        price = request.form['price']
        update_product(product_id, name, quantity, price)  # Chama a função de atualização
        flash("Produto atualizado com sucesso!", "success")
        return redirect(url_for('estoque'))
    return render_template('edit_product.html', product=product)

@app.route('/delete_product/<int:product_id>', methods=['POST'])
def delete_product_route(product_id):
    product = Product.query.get(product_id)  # Busca o produto no banco
    if product:
        db.session.delete(product)  # Exclui o produto
        db.session.commit()  # Salva no banco
        flash("Produto excluído com sucesso!", "success")
    else:
        flash("Produto não encontrado!", "danger")

    return redirect(url_for('estoque'))  # Volta para a lista de produtos



