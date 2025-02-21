from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_socketio import SocketIO, emit
from app.models.database import init_db
from app.models.product import Product
from app.models.user import User, Admin, SuperAdmin
from app.controllers.user_controller import *
from app.controllers.product_controller import *
import os

# Inicializa a aplicação Flask e configura os diretórios de templates e arquivos estáticos
app = Flask(__name__, template_folder="app/views/templates", static_folder="app/views/static")

# Chave secreta para a sessão (melhor definir via variável de ambiente para segurança)
app.secret_key = os.getenv('SECRET_KEY', 'sua_chave_secreta')

# Configuração do banco de dados SQLite
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///estoque.db" 
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Inicializa o banco de dados com a aplicação Flask
init_db(app)

# Inicializa o WebSocket com suporte para threads e permissões para conexões de origens diferentes
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading', ping_interval=5)

# ===================== Rotas da aplicação =====================

# Rota principal que renderiza a página inicial
@app.route("/")
def homepage():
    return render_template("home.html")

# Evento WebSocket para quando um cliente se conecta
@socketio.on("connect")
def handle_connect():
    print("🔌 Cliente conectado!")

# Evento WebSocket para quando um cliente se desconecta
@socketio.on("disconnect")
def handle_disconnect():
    print("🔌 Cliente desconectado!")

# Evento WebSocket para atualizar o estoque em tempo real para todos os clientes conectados
@socketio.on("update_stock")
def handle_update_stock(data):
    socketio.emit("update_stock", data, broadcast=True)  # Broadcast para todos os clientes

# Evento WebSocket para um cliente solicitar os dados do estoque
@socketio.on("request_stock")
def send_stock():
    print("📡 Cliente solicitou atualização do estoque")
    products = Product.query.all()
    stock_data = [{"id": p.id, "name": p.name, "quantity": p.quantity, "price": p.price} for p in products]
    emit("update_stock", stock_data)  # Envia os dados atualizados ao cliente solicitante

# ===================== Rotas de autenticação =====================

# Rota para login (suporta GET para exibir a página e POST para processar o login)
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]  # Obtém o nome de usuário do formulário
        password = request.form["password"]  # Obtém a senha do formulário
        
        # Verifica as credenciais do usuário usando a função de login
        if login_user(username, password):
            flash("Login bem-sucedido!", "success")
            return redirect(url_for("estoque"))  # Redireciona para a página do estoque
        
        flash("Credenciais inválidas!", "danger")  # Mensagem de erro

    return render_template("login.html")  # Exibe a página de login

# Rota para cadastro de novos usuários
@app.route("/cadastro", methods=["GET", "POST"])
def cadastrar():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        
        superadmin = 'superadmin' in request.form
        admin = 'admin' in request.form  # Verifica se a opção admin foi marcada

        # Verifica se o usuário já existe no banco de dados
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Erro: Nome de usuário já está em uso.", "danger")
            return redirect(url_for('cadastrar'))  # Redireciona para o cadastro novamente

        # Cria um novo usuário com permissões apropriadas
        new_user = User(username=username, is_admin=admin, is_super_admin=superadmin)
        new_user.set_password(password)  # Armazena a senha de forma segura
        db.session.add(new_user)
        db.session.commit()
        
        login_user(username, password)  # Faz login automático após o cadastro

        flash("Usuário cadastrado com sucesso!", "success")
        return redirect(url_for("estoque"))  # Redireciona para a página do estoque

    return render_template("cadastro.html")

# Rota para logout
@app.route("/logout")
def logout():
    logout_user()  # Limpa a sessão do usuário
    flash("Você saiu com sucesso.", "success")
    return redirect(url_for("homepage"))  # Redireciona para a página inicial

# ===================== Rotas do estoque =====================

# Rota para exibir a lista de produtos no estoque
@app.route('/estoque')
def estoque():
    products = db.session.query(Product, User.username).join(User).all()  # Busca produtos e seus donos
    return render_template('estoque.html', products=products)

# Atualiza o estoque e emite um evento WebSocket
def atualizar_estoque():
    products = Product.query.all()
    stock_data = [{"id": p.id, "name": p.name, "quantity": p.quantity, "price": p.price} for p in products]
    socketio.emit("update_stock", stock_data)  # Envia para todos os clientes conectados

# Rota para adicionar um novo produto
@app.route('/add_product', methods=['GET', 'POST'])
def add_product_route():
    if request.method == 'POST':
        name = request.form['name']
        quantity = int(request.form['quantity'])
        price = float(request.form['price'])
        add_product(name, quantity, price)  # Função que adiciona o produto ao banco

        # Atualiza o estoque via WebSocket
        socketio.emit("update_stock", {"action": "add", "name": name, "quantity": quantity, "price": price})
        atualizar_estoque()
        flash("Produto adicionado com sucesso!", "success")
        return redirect(url_for('estoque'))  # Redireciona para a página do estoque
    
    return render_template('add_product.html')  # Exibe o formulário para adicionar produtos

# Rota para atualizar um produto existente
@app.route('/update_product/<int:product_id>', methods=['GET', 'POST'])
def update_product_route(product_id):
    product = Product.query.get(product_id)
    if request.method == 'POST':
        name = request.form['name']
        quantity = request.form['quantity']
        price = request.form['price']
        update_product(product_id, name, quantity, price)  # Atualiza no banco de dados

        socketio.emit("update_stock", {"action": "update", "id": product_id, "name": name, "quantity": quantity, "price": price})
        atualizar_estoque()
        flash("Produto atualizado com sucesso!", "success")
        return redirect(url_for('estoque'))
    
    return render_template('update_product.html', product=product)

# Rota para deletar um produto
@app.route('/delete_product/<int:product_id>', methods=['POST'])
def delete_product_route(product_id):
    product = Product.query.get(product_id)  # Busca o produto no banco
    if product:
        db.session.delete(product)  # Remove o produto do banco
        db.session.commit()
        
        socketio.emit("update_stock", {"action": "delete", "id": product_id})
        atualizar_estoque()
        flash("Produto excluído com sucesso!", "success")
    else:
        flash("Produto não encontrado!", "danger")

    return redirect(url_for('estoque'))

# Rota para listar todos os usuários cadastrados
@app.route("/users")
def list_users():
    users = User.query.all()  # Busca todos os usuários
    return render_template('list_users.html', users=users)

# ===================== Inicialização da Aplicação =====================
if __name__ == "__main__":
    port = int(os.getenv('PORT', 5000))  # Usa variável de ambiente para definir a porta
    socketio.run(app, debug=True, host="0.0.0.0", port=port)  # Inicia a aplicação com suporte a WebSockets
