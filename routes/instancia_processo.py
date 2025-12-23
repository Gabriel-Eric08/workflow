from flask import Blueprint, request, jsonify
from services.instancia_processo_service import InstanciaProcessoService

instancia_processo_service= InstanciaProcessoService()
instancia_processo_bp = Blueprint('InstanciaProcesso', __name__)

@instancia_processo_bp.route('/register', methods=['POST'])
def create():
    data = request.get_json()
    if not data:
        return jsonify({
            "sucess":True,
            "message":"No data in request body"
        }), 401
    id_modelo = data.get('id_modelo')
    id_criador = data.get('id_criador')
    data_inicio = data.get('data_inicio')
    status_geral = data.get('status_geral')
    if not id_modelo or not id_criador or not data_inicio or status_geral is None:
        return jsonify({
            "sucess":False,
            "message":"All fields are required in request body"
        }), 422
    create = instancia_processo_service.create(id_modelo,id_criador,data_inicio,status_geral)
    if create:
        return jsonify({
            "sucess":True,
            "message":"New Instancia created"
        }), 200
    return jsonify({
        "sucess":False,
        "message":"Internal server error"
    }), 500