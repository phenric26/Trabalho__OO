from flask import Flask
from route import app  # Importa a aplicação de um módulo externo
import os

# Execução da aplicação se o script for rodado diretamente
if __name__ == "__main__":
    port = int(os.getenv('PORT', 5000))  # Usa variável de ambiente para a porta
    app.run(host='0.0.0.0', port=port, debug=False)  # Garante compatibilidade com sandbox