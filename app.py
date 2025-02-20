from flask import Flask, render_template, request, redirect, url_for, session
import os

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'sua_chave_secreta')  # Usa variável de ambiente para chave secreta

# Usuários fictícios para exemplo
USERS = {
    'usuario': 'senha123',
    'admin': 'admin123'
}

@app.route('/')
def home():
    if 'username' in session:
        return f'Bem-vindo, {session["username"]}! <br><a href="/logout">Logout</a>'
    return 'Você não está logado. <a href="/login">Login</a>'

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in USERS and USERS[username] == password:
            session['username'] = username
            return redirect(url_for('home'))
        else:
            return 'Credenciais inválidas. <a href="/login">Tente novamente</a>'
    return '''
        <form method="post">
            Usuário: <input type="text" name="username"><br>
            Senha: <input type="password" name="password"><br>
            <input type="submit" value="Login">
        </form>
    '''

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))  # Usa variável de ambiente para a porta
    app.run(host='0.0.0.0', port=port, debug=False)  # Garante compatibilidade com sandbox
