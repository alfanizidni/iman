from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models.models import Santri, Lembaga, Kampus
from datetime import datetime
from models import db
import logging

kampus_routes = Blueprint('kampus', __name__)

logger = logging.getLogger('kampus_routes')

@kampus_routes.route('/add_santri', methods=['GET', 'POST'])
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
        logger.info(f"Received data: {nama_santri}, {jenis_kelamin}, {tempat_lahir}, {tanggal_lahir}, {alamat}, {no_telp}, {nama_lembaga}, {jurusan}, {tahun_masuk}, {tahun_lulus}")

        try:
            tanggal_lahir = datetime.strptime(tanggal_lahir, '%Y-%m-%d')
            # tahun_lulus = datetime.strptime(tahun_lulus, '%Y-%m-%d')
        except ValueError:
            flash("Format tanggal salah. Gunakan format YYYY-MM-DD.")
            return redirect(url_for('kampus.add_santri'))

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

        logger.info(f"Creating Kampus: {jurusan_kampus}")


        try:
            db.session.add(new_santri)
            db.session.add(new_lembaga)
            db.session.add(new_kampus)
            db.session.commit()
            logger.info(f"Data Santri dan Lembaga added successfully")
            
            flash('Data santri berhasil ditambahkan!', 'success')
            return redirect(url_for('add_santri'))
        except Exception as e:
            db.session.rollback()
            logger.error(f"Error while adding santri: {str(e)}")
            flash(f'Error: {str(e)}', 'danger')
            return redirect(url_for('kampus.add_santri'))
    
    return render_template('biodata.html')  # Sesuaikan template Anda