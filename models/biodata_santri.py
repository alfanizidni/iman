from . import db # import dari __init__.py

class Santri(db.Model):
    __tablename__ = 'tb_santri'
    id_santri = db.Column(db.Integer, primary_key=True)
    nama_santri = db.Column(db.String(50))
    jenis_kelamin = db.Column(db.String(50))
    tempat_lahir = db.Column(db.String(50))
    tanggal_lahir = db.Column(db.Date, nullable=False)
    alamat = db.Column(db.String(50))
    no_telp = db.Column(db.String(50))

    lembagas = db.relationship('Lembaga', backref='santri', lazy=True)
    kampuss = db.relationship('Kampus', backref='santri', lazy=True)


class Lembaga(db.Model):
    __tablename__ = 'tb_lembaga'
    id_lembaga = db.Column(db.Integer, primary_key=True)
    id_santri = db.Column(db.Integer, db.ForeignKey('tb_santri.id_santri'), nullable=False)
    nama_lembaga = db.Column(db.String(50))
    jurusan = db.Column(db.String(50))
    tahun_masuk = db.Column(db.Date, nullable=False)    
    tahun_lulus = db.Column(db.Date, nullable=False)

class Kampus(db.Model):
    __tablename__ = 'tb_kampus'
    id_kampus = db.Column(db.Integer, primary_key=True)
    id_santri = db.Column(db.Integer, db.ForeignKey('tb_santri.id_santri'), nullable=False)
    nama_kampus = db.Column(db.String(50))
    jurusan = db.Column('jurusan', db.String(50), key='jurusan_kampus')
    program_studi = db.Column(db.String(50))
    organisasi_internal = db.Column(db.String(50))
    organisasi_eksternal = db.Column(db.String(50))
    nama_himpunan = db.Column(db.String(50))
    kota = db.Column(db.String(50))
    provinsi = db.Column(db.String(50))
    tahun_masuk = db.Column('tahun_masuk', db.Date, nullable=False, key='tahun_masuk_kampus' )
    perusahaan = db.Column(db.String(50))
    alamat_perusahaan= db.Column(db.String(50))
    jabatan = db.Column(db.String(50))
