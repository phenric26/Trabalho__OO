from flask import Flask, render_template, url_for

app = Flask(__name__, template_folder=("app/views/templates"))


#Rotas
@app.route("/")
def homepage():
    return render_template("home.html")

@app.route("/login")
def login():
    return render_template("login.html")


