from flask import Blueprint, jsonify, request
from models.models import KampusMaster

kampusMst_routes = Blueprint('kampusMst_routes', __name__)

@kampusMst_routes.route('/', methods=['GET'])
def get_all_kampus():
    kampus_list = KampusMaster.query.all()
    data = [{'id_kampus': k.id_kampus, 'nama_kampus': k.nama_kampus} for k in kampus_list]
    return jsonify(data), 200
