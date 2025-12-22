from flask import Blueprint, jsonify, request
from services.etapa_definicao_service import EtapaDefinicaoService

etapa_definicao_service = EtapaDefinicaoService()
etapa_definicao_bp = Blueprint('EtapaDefinicao', __name__)

@etapa_definicao_bp.route('/register', methods=['POST'])
def create_etapa():
    data = request.get_json()
    if not data:
        return jsonify({
            "sucess":False,
            "message":"No data in body request"
        }), 401
    id_modelo = data.get('id_modelo')
    id_cargo = data.get('id_cargo')
    nome_tarefa = data.get('nome_tarefa')
    ordem_sequencial = data.get('ordem_sequencial')
    requer_anexo = data.get('requer_anexo')
    requer_obs = data.get('requer_obs')
    if (id_modelo is None or 
        id_cargo is None or 
        not nome_tarefa or 
        ordem_sequencial is None or 
        requer_anexo is None or 
        requer_obs is None):
            return jsonify({
                 "sucess": False,
                 "message": "All fields are required in body request"
            }), 422 
    create = etapa_definicao_service.create(id_modelo, id_cargo, nome_tarefa, ordem_sequencial, requer_anexo, requer_obs)
    if create:
         return jsonify({
              "sucess":True,
              "message":"New EtapaDefinicao add"
         }), 200
    return jsonify({
         "sucess":False,
         "message":"Internal server error"
    }), 500