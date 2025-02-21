from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_socketio import SocketIO, emit
from app.models.database import init_db
from app.models.product import Product
from app.models.user import User, Admin, SuperAdmin
from app.controllers.user_controller import *
from app.controllers.product_controller import *
import os
import logging
# Inicializa a aplicação Flask e configura os diretórios de templates e arquivos estáticos
app = Flask(__name__, template_folder=("app/views/templates"), static_folder=("app/views/static"))
app.secret_key = os.getenv('SECRET_KEY', 'sua_chave_secreta')


# Configuração do banco de dados SQLite
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///estoque.db" 

# Inicializa o banco de dados com a aplicação
init_db(app)

# Inicializa o WebSocket
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading', ping_interval=5)


logging.basicConfig(level=logging.DEBUG)
# Rotas da aplicação    

# Rota principal que renderiza a página inicial
@app.route("/")
def homepage():
    return render_template("home.html")

@socketio.on("connect")
def handle_connect():
    print("🔌 Cliente conectado!")

@socketio.on("disconnect")
def handle_disconnect():
    print("🔌 Cliente desconectado!")

# Evento WebSocket para atualizar o estoque em tempo real
@socketio.on("update_stock")
def handle_update_stock(data):
    socketio.emit("update_stock", data, broadcast=True)  # Envia para todos os clientes conectados

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
        
        superadmin = 'superadmin' in request.form
        admin = 'admin' in request.form  # Verifica se a opção admin foi marcada

        # Verifica se o usuário já existe no banco de dados
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash("Erro: Nome de usuário já está em uso.", "danger")
            return redirect(url_for('cadastrar'))  # Redireciona para a página de cadastro

        # Se o nome de usuário for único, cria um novo usuário
        new_user = User(username=username, is_admin=admin, is_super_admin = superadmin)
        new_user.set_password(password)  # Método para armazenar a senha de forma segura
        db.session.add(new_user)
        db.session.commit()
        
        login_user(username, password)


        flash("Usuário cadastrado com sucesso!", "success")
        return redirect(url_for("estoque"))  # Redireciona após cadastro bem-sucedido

    return render_template("cadastro.html")


@app.route("/logout")
def logout():
    logout_user()  # Limpa as informações da sessão
    flash("Você saiu com sucesso.", "success")  # Exibe mensagem de sucesso
    return redirect(url_for("homepage"))

# Rota para exibir a lista de produtos no estoque
@app.route('/estoque')
def estoque():
    # Recupera os produtos e seus donos usando join
    products = db.session.query(Product, User.username).join(User).all()
    return render_template('estoque.html', products=products)
  # Chama a função que lista os produtos

@app.route('/add_product', methods=['GET', 'POST'])
def add_product_route():
    if request.method == 'POST':
        name = request.form['name']
        quantity = int(request.form['quantity'])
        price = float(request.form['price'])
        add_product(name, quantity, price)  # Chama a função add_product para adicionar o produto
        
        logging.debug(f"🔴 Emitindo evento WebSocket para adicionar produto: {name}")
        print(f"✅ Produto '{name}' adicionado, emitindo evento WebSocket")
        

        socketio.emit("update_stock", {"action": "add", "name": name, "quantity": quantity, "price": price})
        
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
        
        socketio.emit("update_stock", {"action": "update", "id": product_id, "name": name, "quantity": quantity, "price": price})
    
        flash("Produto atualizado com sucesso!", "success")
        return redirect(url_for('estoque'))
    return render_template('update_product.html', product=product)

@socketio.on("update_stock")
def update_stock(data):
    print("📡 Enviando atualização de estoque:", data)
    socketio.emit("update_stock", data)  # Envia a todos os clientes


@app.route('/delete_product/<int:product_id>', methods=['POST'])
def delete_product_route(product_id):
    product = Product.query.get(product_id)  # Busca o produto no banco
    if product:
        db.session.delete(product)  # Exclui o produto
        db.session.commit()  # Salva no banco
        
        socketio.emit("update_stock", {"action": "delete", "id": product_id})
        
        flash("Produto excluído com sucesso!", "success")
    else:
        flash("Produto não encontrado!", "danger")

    return redirect(url_for('estoque'))  # Volta para a lista de produtos


@app.route("/users")
def list_users():
    # Lógica para listar os usuários
    users = User.query.all()  # Supondo que você esteja buscando todos os usuários do banco de dados
    return render_template('list_users.html', users=users)


if __name__ == "__main__":
    port = int(os.getenv('PORT', 5000))  # Usa variável de ambiente para a porta
    socketio.run(app, debug=True, host="0.0.0.0", port=port)  # Garante compatibilidade com sandbox


