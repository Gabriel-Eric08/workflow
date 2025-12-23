from flask import Blueprint, request, jsonify
from services.tarefa_execucao_service import TarefaExecucaoService

tarefa_execucao_service=TarefaExecucaoService()
tarefa_execucao_bp = Blueprint('TarefaExecucao', __name__)

@tarefa_execucao_bp.route('/register', methods=['POST'])
def create():
    data = request.get_json()
    if not data:
        return jsonify({
            "sucess":True,
            "message":"No data in request body"
        }), 401
    id_instancia = data.get('id_instancia')
    id_etapa_definicao = data.get('id_etapa_definicao')
    id_funcionario = data.get('id_funcionario')
    status_tarefa = data.get('status_tarefa')
    texto_saida = data.get('texto_saida')
    data_conclusao = data.get('data_conclusao')
    if not id_instancia or not id_etapa_definicao or not id_funcionario or status_tarefa is None or not texto_saida or not data_conclusao:
        return jsonify({
            "sucess":False,
            "message":"All fields are required in request body"
        }), 422
    create = tarefa_execucao_service.create(id_instancia, id_etapa_definicao, id_funcionario, status_tarefa, texto_saida, data_conclusao)
    if create:
        return jsonify({
            "sucess":True,
            "message":"New TarefaExecucao created"
        }), 200
    return jsonify({
        "sucess":False,
        "message":"Internal server error"
    }), 500