from flask import Flask
from route import app  # Importa a aplicação de um módulo externo

# Execução da aplicação se o script for rodado diretamente
if __name__ == "__main__":
    app.run(debug=True)