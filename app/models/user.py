from .database import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
class Person(db.Model):
    __tablename__ = "person"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)

    def get_role(self):
        return "Person"


class User(Person):
    __tablename__ = "user"

    id = db.Column(db.Integer, db.ForeignKey("person.id"), primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

   
    products = db.relationship("Product", back_populates="owner", cascade="all, delete")

    def get_role(self):
        return "Admin" if self.is_admin else "User"