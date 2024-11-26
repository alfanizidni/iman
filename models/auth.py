from . import db # import dari __init__.py
from werkzeug.security import generate_password_hash, check_password_hash

class Auth(db.Model):
    __tablename__ = 'tb_user'
    id_user = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    nama = db.Column(db.String(100), unique=True, nullable=False)
    # user_role = db.Column(db.String(10), unique=True, nullable=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

