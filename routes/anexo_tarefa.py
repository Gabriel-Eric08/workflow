from flask import Blueprint, request, jsonify
from services.anexo_tarefa_service import AnexoTarefaService

anexo_tarefa_service=AnexoTarefaService()
anexo_tarefa_bp = Blueprint('AnexoTarefa', __name__)

@anexo_tarefa_bp.route('/register', methods=['POST'])
def create():
    data = request.get_json()
    if not data:
        return jsonify({
            "sucess":False,
            "message":"No data in body request"
        }), 401 
    id_tarefa_executada = data.get('id_tarefa_executada')
    nome_arquivo = data.get('nome_arquivo')
    url_arquivo = data.get('url_arquivo')
    data_upload = data.get('data_upload')
    if not id_tarefa_executada or nome_arquivo is None or url_arquivo is None or not data_upload:
        return jsonify({
            "sucess":False,
            "message":"All fields are required in request body"
        }), 422
    create = anexo_tarefa_service.create(id_tarefa_executada,nome_arquivo,url_arquivo,data_upload)
    if create:
        return jsonify({
            "sucess":True,
            "message":"New AnexoTarefa created"
        }), 200
    return jsonify({
        "sucess":False,
        "message":"Internal server error"
    }), 500
