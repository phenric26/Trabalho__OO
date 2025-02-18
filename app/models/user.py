from .database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    products = db.relationship("Product", back_populates="owner", cascade="all, delete")

    def get_role(self):
        return "Admin" if self.is_admin else "User"