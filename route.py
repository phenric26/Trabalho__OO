from flask import Flask, render_template, request, redirect, url_for, flash, session
from app.models.database import init_db
from app.models.product import Product
from app.controllers.user_controller import login_user
from app.controllers.product_controller import *

app = Flask(__name__, template_folder=("app/views/templates"), static_folder = ("app/views/static"))

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///estoque.db" 

init_db(app)


#Rotas
@app.route("/")
def homepage():
    return render_template("home.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST": 
        username = request.form["username"]
        password = request.form["password"]
        
        if login_user(username, password):
            flash("Login bem-sucedido!", "success")
            return redirect(url_for("estoque"))
        
        flash("Credenciais inválidas!", "danger")

    return render_template("login.html")  


@app.route("/estoque")
def estoque():
    return list_products()


