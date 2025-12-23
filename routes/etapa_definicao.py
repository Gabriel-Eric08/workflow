from flask import Blueprint, jsonify, request, render_template
from services.etapa_definicao_service import EtapaDefinicaoService

etapa_definicao_service = EtapaDefinicaoService()
etapa_definicao_bp = Blueprint('EtapaDefinicao', __name__)

# --- ROTA GET (NECESSÁRIA PARA A LISTAGEM) ---
@etapa_definicao_bp.route('/by_modelo/<int:id_modelo>', methods=['GET'])
def get_by_modelo(id_modelo):
    try:
        etapas = etapa_definicao_service.get_by_modelo_id(id_modelo)
        # Converte a lista de objetos para lista de dicionários
        etapas_list = [etapa.to_dict() for etapa in etapas]
        
        return jsonify({
            "sucess": True,
            "etapas": etapas_list
        }), 200
    except Exception as e:
        return jsonify({
            "sucess": False,
            "message": "Erro ao buscar etapas"
        }), 500


# --- ROTA POST (CADASTRO) ---
@etapa_definicao_bp.route('/register', methods=['POST'])
def create_etapa():
    data = request.get_json()
    if not data:
        return jsonify({
            "sucess": False,
            "message": "No data in body request"
        }), 401
        
    id_modelo = data.get('id_modelo')
    id_cargo = data.get('id_cargo')
    nome_tarefa = data.get('nome_tarefa')
    descricao = data.get('descricao') # Pegando do JSON (se houver)
    ordem_sequencial = data.get('ordem_sequencial')
    requer_anexo = data.get('requer_anexo')
    requer_obs = data.get('requer_obs')

    # Validação rigorosa
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
            
    # Passando descricao também
    create = etapa_definicao_service.create(id_modelo, id_cargo, nome_tarefa, ordem_sequencial, requer_anexo, requer_obs, descricao)
    
    if create:
         return jsonify({
              "sucess": True,
              "message": "New EtapaDefinicao add"
         }), 200
         
    return jsonify({
         "sucess": False,
         "message": "Internal server error"
    }), 500

@etapa_definicao_bp.route('/fluxo', methods=['GET'])
def etapas_page():
    # Renderiza o template. O ID estará na URL e o JavaScript do template o capturará.
    return render_template('definir_etapas.html')