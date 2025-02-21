# Use uma imagem base do Python
FROM python:3.11-slim

# Define o diretório de trabalho no contêiner
WORKDIR /app

# Copie os arquivos de dependências
COPY requirements.txt requirements.txt

# Instale as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copie todo o código do projeto para dentro do contêiner
COPY . .

# Exponha a porta que a aplicação usará
EXPOSE 5000

# Inicia o aplicativo Flask com SocketIO
CMD ["python", "route.py"]

