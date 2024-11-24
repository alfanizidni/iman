from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
import logging
from flask_migrate import Migrate
from models import db
from models.biodata_santri import Santri, Lembaga, Kampus, KampusMaster, Jurusan, ProgramStudi, Provinsi, Kota
from models.auth import Auth
from flask_bcrypt import Bcrypt
from datetime import datetime
# import os
# os.urandom(24)
# from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
bcrypt = Bcrypt(app)

# import logging
# logging.basicConfig(filename='app.log', level=logging.INFO)

# Menambahkan SECRET_KEY
app.config['SECRET_KEY'] = 'hs174hkuHAHLNNJSJJnnjnxd1234'  # Ganti dengan secret key yang aman

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///alumni_nuris.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/iman'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)
db.init_app(app)

migrate = Migrate(app, db)

# with app.app_context():
#     db.create_all()  # Membuat tabel berdasarkan model
#     print("Tabel berhasil dibuat.")


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
            
            flash('Data santri berhasil ditambahkan!', 'success')
            return redirect(url_for('add_santri'))
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Error while adding santri: {str(e)}")
            flash(f'Error: {str(e)}', 'danger')
            return redirect(url_for('add_santri'))

    return render_template('biodata.html')  # Sesuaikan template Anda

@app.route('/add_data', methods=['POST'])
def add_data():
    try:
        data = request.json

        # Ambil data dari JSON
        nama_kampus = data.get('nama_kampus')
        nama_jurusan = data.get('nama_jurusan')
        nama_program_studi = data.get('nama_program_studi')
        nama_provinsi = data.get('nama_provinsi')
        nama_kota = data.get('nama_kota')

        if not all([nama_kampus, nama_jurusan, nama_program_studi, nama_provinsi, nama_kota]):
            return jsonify({'error': 'Semua field harus diisi'}), 400


        # Buat objek masing-masing model
        provinsi = Provinsi(nama_provinsi=nama_provinsi)
        db.session.add(provinsi)
        db.session.flush()  # Dapatkan ID provinsi
        app.logger.info(f"Inserted Provinsi with id: {provinsi.id_provinsi}")

        kota = Kota(nama_kota=nama_kota, id_provinsi=provinsi.id_provinsi)
        db.session.add(kota)
        db.session.flush()  # Dapatkan ID kota
        app.logger.info(f"Inserted Kota with id: {kota.id_kota}")

        kampus = KampusMaster(
            nama_kampus=nama_kampus,
            alamat_kampus=None,
            id_provinsi=provinsi.id_provinsi,
            id_kota=kota.id_kota
            )
        db.session.add(kampus)
        # db.session.commit()  # Commit terlebih dahulu untuk kampus
        db.session.flush()  # Dapatkan ID kampus
        app.logger.info(f"Inserted Kampus with id: {kampus.id_kampus}")

        # app.logger.error(f"Failed to insert jurusan: {e}")
        # app.logger.info(f"Inserting into tb_jurusan with id_kampus: {kampus.id_kampus}")


        jurusan = Jurusan(nama_jurusan=nama_jurusan, id_kampus=kampus.id_kampus)
        db.session.add(jurusan)
        db.session.flush()  # Dapatkan ID jurusan
        app.logger.info(f"Inserted Jurusan with id: {jurusan.id_jurusan}")

        program_studi = ProgramStudi(nama_program_studi=nama_program_studi, id_jurusan=jurusan.id_jurusan)
        db.session.add(program_studi)
        app.logger.info(f"Inserted ProgramStudi with id: {program_studi.id_program_studi}")

        # Commit perubahan ke database
        db.session.commit()

        app.logger.info(f"Received data: {request.json}")

        # if not all([nama_kampus, nama_jurusan, nama_program_studi, nama_provinsi, nama_kota]):
        #     return jsonify({'error': 'Semua field harus diisi'}), 400

        # # Cek duplikasi kampus
        # existing_kampus = KampusMaster.query.filter_by(nama_kampus=nama_kampus).first()
        # if existing_kampus:
        #     return jsonify({'error': 'Nama kampus sudah ada'}), 400


        return jsonify({'message': 'Data berhasil ditambahkan'}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


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

# @app.route("/kopimanis")
# def kopimanis():
#     return render_template('kopimanis.html', menu='komunitas', submenu='kopimanis')

@app.route("/ikmaris")
def ikmaris():
    return render_template('ikmaris.html', menu='komunitas', submenu='ikmaris')

if __name__ == "__main__":
    app.run(debug=True)

# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000)    
    

