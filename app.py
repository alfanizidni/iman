from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
import logging
from flask_migrate import Migrate
from sqlalchemy.exc import OperationalError
from sqlalchemy.sql import text
from models import db
from models.models import Santri
from models.auth import Auth 
from routes import kampusMst_routes, jurusan_routes, prodi_routes
from routes.kampus_routes import kampus_routes
from routes.auth_routes import auth_bp
from flask_login import LoginManager, login_required


app = Flask(__name__)
app.config['DEBUG'] = True


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
# Middleware untuk pengecekan koneksi database

# Setup LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'  # Rute untuk halaman login


@app.before_request
def check_db_connection():
    try:
        # Query sederhana untuk cek koneksi
        db.session.execute(text('SELECT 1'))
    except OperationalError:
        # Tangani error jika koneksi terputus
        return render_template('error.html', message="Koneksi ke database terputus! Silahkan dicek yagesya"), 500

@login_manager.user_loader
def load_user(user_id):
    return Auth.query.get(int(user_id))  # Memuat pengguna berdasarkan user_id

@app.route("/")
@login_required
def index():
    return redirect(url_for('auth.login'))  # Ganti 'auth.login' sesuai dengan nama fungsi rute login Anda

@app.route("/index")
@login_required
def home():
    return render_template("index.html")  # Render halaman utama

@app.route("/kopimanis")
@login_required
def santri():
    selected_santri = db.session.query(Santri.nama_santri, Santri.jenis_kelamin, Santri.tempat_lahir,
                                       Santri.alamat,Santri.no_telp).all()
    return render_template('kopimanis.html', menu='komunitas', submenu='kopimanis', santri=selected_santri)

@app.route("/tambah_user")
@login_required
def tambah_user():
    return render_template('tambah_user.html', menu='previllege', submenu='tambah_user')

@app.route("/ikmaris")
@login_required
def ikmaris():
    return render_template('ikmaris.html', menu='komunitas', submenu='ikmaris')

if __name__ == "__main__":
    app.run(debug=True)

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000)    
    

