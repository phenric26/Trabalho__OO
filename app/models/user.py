from werkzeug.security import generate_password_hash, check_password_hash
from .database import db
from .product import Product


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_super_admin = db.Column(db.Boolean, default=False)

    products = db.relationship("Product", back_populates="owner", cascade="all, delete")

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_role(self):
        # Implementação padrão do User
        return "User"


class Admin(User):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)  # Chama o construtor da classe User

    def get_role(self):
        return "Admin"


class SuperAdmin(User):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)  # Chama o construtor da classe User

    def get_role(self):
        return "SuperAdmin"

    