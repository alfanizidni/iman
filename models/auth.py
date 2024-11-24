from . import db # import dari __init__.py

class Auth(db.Model):
    __tablename__ = 'tb_user'
    id_user = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    nama = db.Column(db.String(100), unique=True, nullable=False)
    # user_role = db.Column(db.String(10), unique=True, nullable=True)

