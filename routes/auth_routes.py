from flask import Flask, Blueprint, render_template, request, redirect, url_for, session, flash
from models.auth import Auth
from flask_bcrypt import Bcrypt
from models import db
from flask_login import login_user, logout_user, login_required

auth_bp = Blueprint('auth', __name__)
bcrypt = Bcrypt()


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # print(request.form)
        identifier = request.form.get("identifier")
        password = request.form.get("password")
        
        # Cek apakah user dengan email tersebut ada di database
        user = Auth.query.filter((Auth.email == identifier) | (Auth.nama == identifier)).first()

        # Jika user ada dan password cocok, redirect ke halaman dashboard
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            # session['auth.user_id'] = user.id_user
            # session['auth.username'] = user.nama
            return redirect(url_for('home'))
        else:
            # Jika login gagal, tampilkan pesan error
            flash("Nama, Email atau password salah", "danger")
            return redirect(url_for('auth.login'))   

    return render_template('auth/login.html')

@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()  # Logout menggunakan Flask-Login
    session.clear()  # Menghapus semua data dari session
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