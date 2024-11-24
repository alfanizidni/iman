# from sqlalchemy import create_engine

# engine = create_engine('mysql+pymysql://root:@localhost/alumni_nuris')
# connection = engine.connect()
# print("Connected!")
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/iman'
db = SQLAlchemy(app)
migrate = Migrate(app, db)


with app.app_context():
    db.create_all()
