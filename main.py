from flask import Flask

app = Flask(__name__, template_folder="app/templates")

from route import *


if __name__ == "__main__":
    app.run()