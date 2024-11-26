from flask import Blueprint, jsonify, request
from models.models import KampusJurusan, Jurusan

jurusan_routes = Blueprint('jurusan_routes', __name__)

@jurusan_routes.route('/<int:id_kampus>', methods=['GET'])
def get_jurusan_by_kampus(id_kampus):
    jurusan_list = KampusJurusan.query.filter_by(id_kampus=id_kampus).all()
    data = [{'id_jurusan': j.jurusan.id_jurusan, 'nama_jurusan': j.jurusan.nama_jurusan} for j in jurusan_list]
    return jsonify(data), 200
