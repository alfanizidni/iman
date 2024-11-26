from flask import Flask, Blueprint, render_template, request, redirect, url_for, session, flash
from models.auth import Auth
from flask_bcrypt import Bcrypt
from models import db


auth_bp = Blueprint('auth', __name__)
bcrypt = Bcrypt()

# @auth_bp.route("/")
# def home():
#     return redirect(url_for('auth.login'))

@auth_bp.route("/index")
def index():
    return render_template('index.html')

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # print(request.form)
        identifier = request.form.get("identifier")
        password = request.form.get("password")

        # cek input
        # print(f"Identifier: {identifier}")
        # print(f"Password: {password}")
        
        # Cek apakah user dengan email tersebut ada di database
        user = Auth.query.filter((Auth.email == identifier) | (Auth.nama == identifier)).first()

        # Jika user ada dan password cocok, redirect ke halaman dashboard
        if user and bcrypt.check_password_hash(user.password, password):

            session['user_id'] = user.id_user
            session['username'] = user.nama
            return redirect(url_for('auth.index'))
        else:
            # Jika login gagal, tampilkan pesan error
            flash("Nama, Email atau password salah", "danger")
            return redirect(url_for('auth.login'))   

    return render_template('auth/login.html')

@auth_bp.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)  # Menghapus sesi username
    flash('Anda telah logout', 'info')
    return redirect(url_for('auth.login'))  # Arahkan kembali ke halaman login


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        nama = request.form["nama"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        # print(f"Received Username: {nama}, Email: {email}, Password: {password}")  # Debugging

        if password != confirm_password:
            flash("Password dan Konfirmasi Password tidak sama", "danger")
            return redirect(url_for('auth.register'))
        
        existing_user = Auth.query.filter((Auth.email == email) | (Auth.nama == nama)).first()

        if existing_user:
            flash("Nama atau Email sudah terdaftar, Silahkan gunakan yang lain!!", "danger")
            return redirect(url_for('auth.register'))

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Simpan data user baru
        new_user = Auth(nama=nama, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        # print("User added and committed")  # Debugging
        
        flash("Akun berhasil dibuat! Silahkan Login", "success")
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html')