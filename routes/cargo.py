from flask import Blueprint, jsonify, request   
from services.cargo_service import CargoService

cargo_service = CargoService()
cargo_bp = Blueprint('Cargo',__name__)

@cargo_bp.route('/create', methods=['POST'])
def create_cargo():
    data = request.get_json()
    if not data:
        return jsonify({
            "sucess":False,
            "message":"No data in request!"
        }), 401
    name = data.get('name')
    description = data.get('description')
    if not name or not description:
        return jsonify({
            "sucess":False,
            "message": "No name or no description in request!"
        }), 401
    create = cargo_service.create_cargo(name,description)
    if create:
        return jsonify({
            "sucess":True,
            "message":"Cargo created with sucess!"
        }), 200
    return jsonify({
        "sucess":False,
        "message":"Internal error"
    }), 500

@cargo_bp.route('/all', methods=['GET'])
def get_all():
    try:
        cargos = cargo_service.get_all()
        
        # Converte cada objeto Cargo para dicionário
        cargos_list = [cargo.to_dict() for cargo in cargos]
        
        return jsonify({
            "sucess": True,
            "cargos": cargos_list
        }), 200
        
    except Exception as e:
        # Só retorna 500 se realmente der um erro de servidor (exceção)
        print(f"Erro na rota: {e}")
        return jsonify({
            "sucess": False,
            "message": "Internal server error"
        }), 500