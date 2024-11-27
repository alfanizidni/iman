from flask import Blueprint, jsonify, request
from models.models import KampusMaster
from flask_login import LoginManager, login_required

kampusMst_routes = Blueprint('kampusMst_routes', __name__)

# Setup Flask-Login
login_manager = LoginManager()
login_manager.init_app(kampusMst_routes)
login_manager.login_view = 'auth.login'  # Redirect ke login jika belum login

@kampusMst_routes.route('/', methods=['GET'])
def get_all_kampus():
    kampus_list = KampusMaster.query.all()
    data = []
    
    # Menambahkan print untuk memastikan data ada
    if not kampus_list:
        print("Tidak ada data di kampus_list")

    for k in kampus_list:
        print(f"ID Kampus: {k.id_kampus}, Nama Kampus: {k.nama_kampus}")
        print(f"Provinsi: {k.provinsi}, Kota: {k.kota}")  # Memastikan relasi data
        data.append({
            'id_kampus': k.id_kampus,
            'nama_kampus': k.nama_kampus,
            'id_provinsi': k.id_provinsi,
            'id_kota': k.id_kota,
            # 'nama_provinsi': k.provinsi.nama_provinsi if k.provinsi else None,
            # 'nama_kota': k.kota.nama_kota if k.kota else None
        })
    
    print(f"Data : {data}")
    return jsonify(data), 200

@kampusMst_routes.route('/search', methods=['GET'])
def search_kampus():
    query = request.args.get('query')
    kampus_list = KampusMaster.query.filter(KampusMaster.nama_kampus.like(f"%{query}%")).all()
    data = [{'id_kampus': k.id_kampus, 'nama_kampus': k.nama_kampus} for k in kampus_list]
    return jsonify(data), 200

