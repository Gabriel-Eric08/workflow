from flask import Blueprint, request, jsonify, render_template
from services.modelo_processo_service import ModeloProcessoService

modelo_processo_service = ModeloProcessoService()
modelo_processo_bp = Blueprint('ModeloProceso', __name__)

@modelo_processo_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data:
        return jsonify({
            "sucess":False,
            "message":"No data in body request"
        }), 401
    nome_processo = data.get('nome_processo')
    codigo_processo = data.get('codigo_processo')
    descricao = data.get('descricao')
    if nome_processo is None or codigo_processo is None or descricao is None:
        return jsonify({
            "sucess":False,
            "message":"All fields are required in body request"
        }), 422
    create = modelo_processo_service.create(nome_processo,codigo_processo,descricao)
    if create:
        return jsonify({
              "sucess":True,
              "message":"New ModeloProcesso add"
         }), 200
    return jsonify({
        "sucess":False,
        "message":"Internal server error"
    }), 500

@modelo_processo_bp.route('/all', methods=['GET'])
def get_all():
    try:
        modelos = modelo_processo_service.get_all()
        
        # Converte cada objeto Cargo para dicionário
        modelos_list = [modelo.to_dict() for modelo in modelos]
        
        return jsonify({
            "sucess": True,
            "cargos": modelos_list
        }), 200
        
    except Exception as e:
        # Só retorna 500 se realmente der um erro de servidor (exceção)
        print(f"Erro na rota: {e}")
        return jsonify({
            "sucess": False,
            "message": "Internal server error"
        }), 500
    
@modelo_processo_bp.route('/')
def modelo_processo_page():
    return render_template('cadastro_modelo.html')