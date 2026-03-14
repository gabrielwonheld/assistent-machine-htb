from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_login import UserMixin
from extensions import db




class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    image_profile = db.Column(db.String(255))

    def __repr__(self):
        return f"<User {self.username}>"

    def set_password(self, pswd):
        self.password = generate_password_hash(pswd)

    def check_password(self, pswd):
        return check_password_hash(self.password, pswd)

    def update_profile(self, data):
        for key, value in data.items():
            if 'password' in key:
                self.set_password(value)
                continue
            setattr(self, key, value)

class Produto(db.Model):
    __tablename__ = 'produtos'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text)
    ficha_tecnica_path = db.Column(db.String(255)) 
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Produto {self.name}>'

class Client(db.Model):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)

class Venda(db.Model):
    __tablename__ = 'vendas'
    id = db.Column(db.Integer, primary_key=True)
    produto_id = db.Column(db.Integer, db.ForeignKey('produtos.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    quantidade = db.Column(db.Integer, default=1)
    data_venda = db.Column(db.DateTime, default=datetime.utcnow)
    valor_total = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f'<Venda ID {self.id} - Total {self.valor_total}>'