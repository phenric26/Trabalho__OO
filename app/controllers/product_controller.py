from flask import render_template, request, redirect, url_for, flash
from app.models.product import Product
from app.models.database import db

def list_products():
    products = Product.query.all()
    return render_template('estoque.html', products=products)

def add_product(name, quantity, price):
    product = Product(name=name, quantity=quantity, price=price)
    db.session.add(product)
    db.session.commit()

def update_product(product_id, name, quantity, price):
    product = Product.query.get(product_id)
    if product:
        product.name = name
        product.quantity = quantity
        product.price = price
        db.session.commit()

def delete_product(product_id):
    product = Product.query.get(product_id)
    if product:
        db.session.delete(product)
        db.session.commit()
