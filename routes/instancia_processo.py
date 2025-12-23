from flask import Blueprint, request, jsonify, render_template
from services.instancia_processo_service import InstanciaProcessoService

instancia_processo_bp = Blueprint('instancia_processo_bp', __name__)
service = InstanciaProcessoService()

# ==========================================
#  ROTAS DE PÁGINAS (Frontend)
# ==========================================

@instancia_processo_bp.route('/caixa-entrada')
def page_caixa_entrada():
    """Renderiza a página HTML da Caixa de Entrada / Minhas Tarefas"""
    return render_template('caixa_entrada.html') 

# ==========================================
#  ROTAS DE API (Backend / JSON)
# ==========================================

# 1. INICIAR PROCESSO
# Substitui o antigo '/register'. Agora é mais simples.
@instancia_processo_bp.route('/api/iniciar', methods=['POST'])
def iniciar_processo():
    data = request.get_json()
    
    if not data:
        return jsonify({"sucess": False, "message": "No data in request body"}), 400
    
    # Pegamos apenas o Modelo e o Usuário. 
    # Data e Status são gerados automaticamente pelo Repository.
    id_modelo = data.get('id_modelo')
    id_criador = data.get('id_criador') # Em produção, pegue da sessão do usuário logado
    
    resultado = service.iniciar_processo(id_modelo, id_criador)
    
    if resultado.get('sucess'):
        return jsonify(resultado), 200
    else:
        return jsonify(resultado), 500


# 2. LISTAR TAREFAS (Caixa de Entrada)
@instancia_processo_bp.route('/api/minhas-tarefas', methods=['POST'])
def get_tarefas():
    data = request.get_json()
    
    # Precisamos saber quem é o usuário para filtrar as tarefas do cargo dele
    id_usuario = data.get('id_usuario') 
    
    tarefas = service.get_minhas_tarefas(id_usuario)
    
    # Retorna sempre 200, mesmo que a lista seja vazia
    return jsonify({
        "sucess": True, 
        "tarefas": tarefas
    }), 200


# 3. CONCLUIR TAREFA (Avançar Etapa)
@instancia_processo_bp.route('/api/concluir-tarefa', methods=['POST'])
def concluir_tarefa():
    data = request.get_json()
    
    id_tarefa = data.get('id_tarefa')
    id_usuario = data.get('id_usuario')
    texto_saida = data.get('texto_saida') # Opcional (ex: observações)
    
    resultado = service.concluir_tarefa(id_tarefa, id_usuario, texto_saida)
    
    if resultado.get('sucess'):
        return jsonify(resultado), 200
    else:
        return jsonify(resultado), 500