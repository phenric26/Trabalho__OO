from flask import render_template, request, redirect, url_for, flash, session
from app.models.product import Product
from app.models.database import db

# Lista todos os produtos do banco de dados e os renderiza na página de estoque
def list_products():
    products = Product.query.all()
    return render_template('estoque.html', products=products)

# Adiciona um novo produto ao banco de dados
def add_product(name, quantity, price):
    owner_id = session.get('user_id')
    product = Product(name=name, quantity=quantity, price=price, owner_id=owner_id)
    db.session.add(product)  # Adiciona o produto à sessão
    db.session.commit()  # Confirma a transação no banco

# Atualiza os dados de um produto existente no banco de dados
def update_product(product_id, name, quantity, price):
    product = Product.query.get(product_id)  # Busca o produto pelo ID
    if product:
        product.name = name
        product.quantity = quantity
        product.price = price
        db.session.commit()  # Salva as alterações

# Deleta um produto do banco de dados
def delete_product(product_id):
    product = Product.query.get(product_id)  # Busca o produto pelo ID
    if product:
        db.session.delete(product)  # Remove o produto do banco
        db.session.commit()  # Confirma a remoção   