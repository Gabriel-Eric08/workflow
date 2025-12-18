from flask import Blueprint, request, jsonify
from services.funcionario_service import FuncionarioService

funcionario_service = FuncionarioService()

funcionario_bp = Blueprint('Funcionario', __name__)

@funcionario_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        return jsonify({
            "sucess": False,
            "message":"No data in request body"
        }), 401
    id_cargo = data.get('id_cargo')
    nome = data.get('nome')
    email = data.get('email')
    senha = data.get('senha')
    ativo = data.get('ativo')
    if not id_cargo or not nome or not email or not senha or not ativo:
        return jsonify({
            "sucess":False,
            "message":"All fields are requireds!"
        }), 401
    create = funcionario_service.create(id_cargo,nome,email,senha,ativo)
    if create:
        return jsonify({
            "sucess":True,
            "message":"Funcionario created with sucess"
        }), 200
    return jsonify({
        "sucess":False,
        "message":"Internal server error"
    }), 500