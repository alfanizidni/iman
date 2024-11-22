from flask import Flask, render_template, request, redirect, url_for, flash, session
import logging
from models import db
from models.biodata_santri import Santri
from models.biodata_santri import Lembaga
from models.biodata_santri import Kampus
from models.auth import Auth
from flask_bcrypt import Bcrypt
from datetime import datetime
import os
os.urandom(24)
# from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
bcrypt = Bcrypt(app)

# Menambahkan SECRET_KEY
app.config['SECRET_KEY'] = 'hs174hkuHAHLNNJSJJnnjnxd1234'  # Ganti dengan secret key yang aman

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///alumni_nuris.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/alumni_nuris'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)
db.init_app(app)

@app.route("/")
def home():
    return redirect(url_for('login'))

@app.route("/index")
def index():
    return render_template('index.html')

@app.route("/login", methods=["GET", "POST"])
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
            return redirect(url_for('index'))
        else:
            # Jika login gagal, tampilkan pesan error
            flash("Nama, Email atau password salah", "danger")
            return redirect(url_for('login'))   

    return render_template('auth/login.html')

@app.route('/logout', methods=['POST'])
def logout():
    session.pop('username', None)  # Menghapus sesi username
    return redirect(url_for('login'))  # Arahkan kembali ke halaman login


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        nama = request.form["nama"]
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        # print(f"Received Username: {nama}, Email: {email}, Password: {password}")  # Debugging

        if password != confirm_password:
            flash("Password dan Konfirmasi Password tidak sama", "danger")
            return redirect(url_for('register'))
        
        existing_user = Auth.query.filter((Auth.email == email) | (Auth.nama == nama)).first()

        if existing_user:
            flash("Nama atau Email sudah terdaftar, Silahkan gunakan yang lain!!", "danger")
            return redirect(url_for('register'))

        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Simpan data user baru
        new_user = Auth(nama=nama, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        # print("User added and committed")  # Debugging
        
        flash("Akun berhasil dibuat! Silahkan Login", "success")
        return redirect(url_for('login'))
    return render_template('auth/register.html')

@app.route('/add_santri', methods=['GET', 'POST'])
def add_santri():
    if request.method == 'POST':
        nama_santri = request.form.get('nama_santri')
        jenis_kelamin = request.form.get('jenis_kelamin')
        tempat_lahir = request.form.get('tempat_lahir')
        tanggal_lahir = request.form.get('tanggal_lahir')
        alamat = request.form.get('alamat')
        no_telp= request.form.get('no_telp')
        nama_lembaga= request.form.get('nama_lembaga')
        jurusan= request.form.get('jurusan')
        tahun_masuk= request.form.get('tahun_masuk')
        tahun_lulus= request.form.get('tahun_lulus')
        nama_kampus= request.form.get('nama_kampus')
        jurusan_kampus= request.form.get('jurusan')
        program_studi= request.form.get('program_studi')
        organisasi_internal= request.form.get('organisasi_internal')
        organisasi_eksternal= request.form.get('organisasi_eksternal')
        nama_himpunan= request.form.get('nama_himpunan')
        provinsi= request.form.get('provinsi')
        kota= request.form.get('kota')
        tahun_masuk_kampus= request.form.get('tahun_masuk')
        perusahaan= request.form.get('perusahaan')
        alamat_perusahaan= request.form.get('alamat_perusahaan')
        jabatan= request.form.get('jabatan')

        # Log data yang diterima
        app.logger.info(f"Received data: {nama_santri}, {jenis_kelamin}, {tempat_lahir}, {tanggal_lahir}, {alamat}, {no_telp}, {nama_lembaga}, {jurusan}, {tahun_masuk}, {tahun_lulus}")

        try:
            tanggal_lahir = datetime.strptime(tanggal_lahir, '%Y-%m-%d')
            # tahun_lulus = datetime.strptime(tahun_lulus, '%Y-%m-%d')
        except ValueError:
            flash("Format tanggal salah. Gunakan format YYYY-MM-DD.")
            return redirect(url_for('add_santri'))

        new_santri = Santri(
            nama_santri=nama_santri,
            jenis_kelamin=jenis_kelamin,
            tempat_lahir=tempat_lahir,
            tanggal_lahir=tanggal_lahir,
            alamat=alamat,
            no_telp=no_telp            
        )

        new_lembaga = Lembaga(
            nama_lembaga=nama_lembaga,
            jurusan=jurusan,
            tahun_masuk=datetime.strptime(tahun_masuk, '%Y-%m-%d'),
            tahun_lulus=datetime.strptime(tahun_lulus, '%Y-%m-%d'),
            santri=new_santri
        )

        new_kampus = Kampus(
            nama_kampus=nama_kampus,
            jurusan=jurusan_kampus,
            program_studi=program_studi,
            organisasi_internal=organisasi_internal,
            organisasi_eksternal=organisasi_eksternal,
            nama_himpunan=nama_himpunan,
            provinsi=provinsi,
            kota=kota,
            tahun_masuk=datetime.strptime(tahun_masuk_kampus, '%Y-%m-%d'),
            perusahaan=perusahaan,
            alamat_perusahaan=alamat_perusahaan,
            jabatan=jabatan,           
            santri=new_santri
        )

        app.logger.info(f"Creating Kampus: {jurusan_kampus}")


        try:
            db.session.add(new_santri)
            db.session.add(new_lembaga)
            db.session.add(new_kampus)
            db.session.commit()
            app.logger.info(f"Data Santri dan Lembaga added successfully")

            # insert data tabel lembaga
            # santri_id = new_santri.id_santri

            # new_lembaga = Lembaga(nama_lembaga-nama_lembaga, id_santri=santri_id)

            # db.session.add(new_lembaga)
            # db.session.commit

            # app.logger.info("Data lembaga {nama_santri} berhasil diinput")
            
            flash('Data santri berhasil ditambahkan!', 'success')
            return redirect(url_for('add_santri'))
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Error while adding santri: {str(e)}")
            flash(f'Error: {str(e)}', 'danger')
            return redirect(url_for('add_santri'))

    return render_template('ikmaris.html')  # Sesuaikan template Anda


@app.route("/kopimanis")
def santri():
    selected_santri = db.session.query(Santri.nama_santri, Santri.jenis_kelamin, Santri.tempat_lahir,
                                       Santri.alamat,Santri.no_telp).all()
    return render_template('kopimanis.html', menu='komunitas', submenu='kopimanis', santri=selected_santri)

@app.route("/tambah_user")
def tambah_user():
    return render_template('tambah_user.html', menu='previllege', submenu='tambah_user')

@app.route("/hak_akses")
def hak_akses(): 
    return render_template('hak_akses.html', menu='previllege', submenu='hak_akses')

# @app.route("/kopimanis")
# def kopimanis():
#     return render_template('kopimanis.html', menu='komunitas', submenu='kopimanis')

@app.route("/ikmaris")
def ikmaris():
    return render_template('ikmaris.html', menu='komunitas', submenu='ikmaris')

if __name__ == "__main__":
    app.run()

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000)    
    

