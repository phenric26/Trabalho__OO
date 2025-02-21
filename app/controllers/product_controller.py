from flask import render_template, request, redirect, url_for, flash, session
from app.models.product import Product
from app.models.database import db

# ===================== Função para listar todos os produtos =====================

def list_products():
    """
    Consulta todos os produtos do banco de dados e os passa para a página HTML de estoque.

    Retorna:
        Um template renderizado ('estoque.html') contendo a lista de produtos.
    """
    products = Product.query.all()  # Consulta todos os produtos cadastrados no banco
    return render_template('estoque.html', products=products)  # Renderiza a página com os produtos

# ===================== Função para adicionar um novo produto =====================

def add_product(name, quantity, price):
    """
    Adiciona um novo produto ao banco de dados.

    Parâmetros:
        name (str): Nome do produto.
        quantity (int): Quantidade do produto disponível no estoque.
        price (float): Preço unitário do produto.

    Retorno:
        Nenhum. O produto é salvo no banco de dados.

    Observação:
        - O ID do proprietário do produto (usuário logado) é obtido através da sessão.
        - O produto é adicionado ao banco de dados e salvo permanentemente.
    """
    owner_id = session.get('user_id')  # Obtém o ID do usuário logado na sessão
    if owner_id is None:
        flash("Erro: Usuário não autenticado!", "danger")  # Exibe uma mensagem caso o usuário não esteja logado
        return

    # Cria um novo objeto Produto com os dados informados
    product = Product(name=name, quantity=quantity, price=price, owner_id=owner_id)

    db.session.add(product)  # Adiciona o produto à sessão do banco de dados
    db.session.commit()  # Salva as mudanças no banco de dados

# ===================== Função para atualizar um produto existente =====================

def update_product(product_id, name, quantity, price):
    """
    Atualiza os dados de um produto já existente no banco de dados.

    Parâmetros:
        product_id (int): Identificador único do produto.
        name (str): Novo nome do produto.
        quantity (int): Nova quantidade do produto no estoque.
        price (float): Novo preço do produto.

    Retorno:
        Nenhum. Os dados do produto são atualizados no banco de dados.

    Observação:
        - O produto é localizado no banco de dados pelo seu ID.
        - Se o produto for encontrado, seus atributos são modificados e a alteração é salva.
    """
    product = Product.query.get(product_id)  # Busca o produto no banco de dados pelo ID

    if product:  # Verifica se o produto foi encontrado
        product.name = name  # Atualiza o nome do produto
        product.quantity = quantity  # Atualiza a quantidade no estoque
        product.price = price  # Atualiza o preço do produto
        db.session.commit()  # Salva as alterações no banco de dados

# ===================== Função para deletar um produto =====================

def delete_product(product_id):
    """
    Remove um produto do banco de dados.

    Parâmetros:
        product_id (int): Identificador único do produto a ser deletado.

    Retorno:
        Nenhum. O produto é removido do banco de dados.

    Observação:
        - O produto é localizado no banco de dados pelo seu ID.
        - Se o produto for encontrado, ele é deletado e as alterações são salvas.
    """
    product = Product.query.get(product_id)  # Busca o produto no banco de dados pelo ID

    if product:  # Verifica se o produto foi encontrado
        db.session.delete(product)  # Remove o produto do banco de dados
        db.session.commit()  # Confirma a exclusão do produto no banco de dados
