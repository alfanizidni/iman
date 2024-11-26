from flask import Blueprint, jsonify
from models.models import ProgramStudi

prodi_routes = Blueprint('prodi_routes', __name__)

@prodi_routes.route('/<int:id_jurusan>', methods=['GET'])
def get_program_studi_by_jurusan(id_jurusan):
    prodi_list = ProgramStudi.query.filter_by(id_jurusan=id_jurusan).all()
    data = [{'id_prodi': p.id_program_studi, 'nama_prodi': p.nama_program_studi} for p in prodi_list]
    return jsonify(data), 200
