from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
import logging
from flask_migrate import Migrate
from models import db
from models.models import Santri
from routes import kampusMst_routes, jurusan_routes, prodi_routes
from routes.kampus_routes import kampus_routes
from routes.auth_routes import auth_bp

app = Flask(__name__)


# Menambahkan SECRET_KEY
app.config['SECRET_KEY'] = 'hs174hkuHAHLNNJSJJnnjnxd1234'  # Ganti dengan secret key yang aman

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///alumni_nuris.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/iman'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)
db.init_app(app)

app.register_blueprint(kampusMst_routes, url_prefix='/kampusMst')
app.register_blueprint(jurusan_routes, url_prefix='/jurusan')
app.register_blueprint(prodi_routes, url_prefix='/prodi')
app.register_blueprint(kampus_routes, url_prefix='/kampus')
app.register_blueprint(auth_bp, url_prefix='/auth')

migrate = Migrate(app, db)

@app.route("/")
def home():
    return redirect(url_for("auth.login"))  # Pastikan auth.login adalah endpoint yang sesuai

@app.route("/kopimanis")
def santri():
    selected_santri = db.session.query(Santri.nama_santri, Santri.jenis_kelamin, Santri.tempat_lahir,
                                       Santri.alamat,Santri.no_telp).all()
    return render_template('kopimanis.html', menu='komunitas', submenu='kopimanis', santri=selected_santri)

@app.route("/tambah_user")
def tambah_user():
    return render_template('tambah_user.html', menu='previllege', submenu='tambah_user')

@app.route("/add_biodata")
def hak_akses(): 
    return render_template('biodata.html', menu='previllege', submenu='add_biodata')

@app.route("/ikmaris")
def ikmaris():
    return render_template('ikmaris.html', menu='komunitas', submenu='ikmaris')

if __name__ == "__main__":
    app.run(debug=True)

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000)    
    

