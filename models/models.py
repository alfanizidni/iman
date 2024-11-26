from . import db # import dari __init__.py

class Santri(db.Model):
    __tablename__ = 'tb_santri'
    id_santri = db.Column(db.Integer, primary_key=True)
    nama_santri = db.Column(db.String(100))
    jenis_kelamin = db.Column(db.String(100))
    tempat_lahir = db.Column(db.String(100))
    tanggal_lahir = db.Column(db.Date, nullable=False)
    alamat = db.Column(db.String(100))
    no_telp = db.Column(db.String(100))

    lembagas = db.relationship('Lembaga', backref='santri', lazy='joined')
    kampuss = db.relationship('Kampus', backref='santri', lazy='joined')


class Lembaga(db.Model):
    __tablename__ = 'tb_lembaga'
    id_lembaga = db.Column(db.Integer, primary_key=True)
    id_santri = db.Column(db.Integer, db.ForeignKey('tb_santri.id_santri'), nullable=False)
    nama_lembaga = db.Column(db.String(100))
    jurusan = db.Column(db.String(100))
    tahun_masuk = db.Column(db.Date, nullable=False)    
    tahun_lulus = db.Column(db.Date, nullable=False)

class Kampus(db.Model):
    __tablename__ = 'tb_kampus'
    id_kampus = db.Column(db.Integer, primary_key=True)
    id_santri = db.Column(db.Integer, db.ForeignKey('tb_santri.id_santri'), nullable=False)
    nama_kampus = db.Column(db.String(100))
    jurusan = db.Column('jurusan', db.String(100), key='jurusan_kampus')
    program_studi = db.Column(db.String(100))
    organisasi_internal = db.Column(db.String(100))
    organisasi_eksternal = db.Column(db.String(100))
    nama_himpunan = db.Column(db.String(100))
    kota = db.Column(db.String(100))
    provinsi = db.Column(db.String(100))
    tahun_masuk = db.Column('tahun_masuk', db.Date, nullable=False, key='tahun_masuk_kampus' )
    perusahaan = db.Column(db.String(100))
    alamat_perusahaan= db.Column(db.String(100))
    jabatan = db.Column(db.String(100))

class KampusMaster(db.Model):
    __tablename__ = 'tb_mstkampus'
    id_kampus = db.Column(db.Integer, primary_key=True)
    nama_kampus = db.Column(db.String(100), nullable=False)
    alamat_kampus = db.Column(db.String(100))
    id_provinsi = db.Column(db.Integer, db.ForeignKey('tb_provinsi.id_provinsi'), nullable=False)
    id_kota = db.Column(db.Integer, db.ForeignKey('tb_kota.id_kota'), nullable=False)
    provinsi = db.relationship('Provinsi', backref='kampus', lazy=True)
    kota = db.relationship('Kota', backref='kampus', lazy=True)
    kampus_jurusan = db.relationship('KampusJurusan', backref='kampus', lazy=True)


class Jurusan(db.Model):
    __tablename__ = 'tb_jurusan'
    id_jurusan = db.Column(db.Integer, primary_key=True)
    nama_jurusan = db.Column(db.String(100), nullable=False)
    kampus_jurusan = db.relationship('KampusJurusan', backref='jurusan', lazy=True)
    program_studi = db.relationship('ProgramStudi', backref='jurusan', lazy=True)


class KampusJurusan(db.Model):
    __tablename__ = 'tb_kampus_jurusan'
    id = db.Column(db.Integer, primary_key=True)
    id_kampus = db.Column(db.Integer, db.ForeignKey('tb_mstkampus.id_kampus'), nullable=False)
    id_jurusan = db.Column(db.Integer, db.ForeignKey('tb_jurusan.id_jurusan'), nullable=False)


class ProgramStudi(db.Model):
    __tablename__ = 'tb_program_studi'
    id_program_studi = db.Column(db.Integer, primary_key=True)
    nama_program_studi = db.Column(db.String(100), nullable=False)
    id_jurusan = db.Column(db.Integer, db.ForeignKey('tb_jurusan.id_jurusan'), nullable=False)


class Provinsi(db.Model):
    __tablename__ = 'tb_provinsi'
    id_provinsi = db.Column(db.Integer, primary_key=True)
    nama_provinsi = db.Column(db.String(100), nullable=False)
    kota = db.relationship('Kota', backref='provinsi', lazy=True)


class Kota(db.Model):
    __tablename__ = 'tb_kota'
    id_kota = db.Column(db.Integer, primary_key=True)
    nama_kota = db.Column(db.String(100), nullable=False)
    id_provinsi = db.Column(db.Integer, db.ForeignKey('tb_provinsi.id_provinsi'), nullable=False)

