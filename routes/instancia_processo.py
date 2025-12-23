from flask import Blueprint, request, jsonify, render_template
from services.instancia_processo_service import InstanciaProcessoService

instancia_processo_bp = Blueprint('instancia_processo_bp', __name__)
service = InstanciaProcessoService()

# --- PÁGINAS ---

@instancia_processo_bp.route('/dashboard')
def page_dashboard():
    return render_template('dashboard.html')

@instancia_processo_bp.route('/caixa-entrada')
def page_caixa_entrada():
    return render_template('caixa_entrada.html')

# [NOVO] Rota para a página de detalhes/timeline
@instancia_processo_bp.route('/detalhes/<int:id_instancia>')
def page_detalhes(id_instancia):
    # Passamos o id apenas se quiser usar no Jinja, mas o JS vai pegar da URL também
    return render_template('detalhes_processo.html', id_instancia=id_instancia)

# --- API ---

# 1. Obter Lista de Modelos (Para o Dropdown)
@instancia_processo_bp.route('/api/modelos', methods=['GET'])
def api_get_modelos():
    lista = service.get_modelos_dropdown()
    return jsonify(lista)

# 2. Obter Todas as Instâncias (Para a Tabela Geral)
@instancia_processo_bp.route('/api/todas-instancias', methods=['GET'])
def api_get_todas_instancias():
    lista = service.get_todas_instancias()
    return jsonify(lista)

# 3. Iniciar Processo
@instancia_processo_bp.route('/api/iniciar', methods=['POST'])
def api_iniciar():
    data = request.get_json()
    id_modelo = data.get('id_modelo')
    id_criador = data.get('id_criador')
    
    resultado = service.iniciar_processo(id_modelo, id_criador)
    
    status_code = 200 if resultado.get('sucess') else 500
    return jsonify(resultado), status_code

# 4. Minhas Tarefas (Caixa de Entrada antiga)
@instancia_processo_bp.route('/api/minhas-tarefas', methods=['POST'])
def api_minhas_tarefas():
    data = request.get_json()
    id_usuario = data.get('id_usuario')
    tarefas = service.get_minhas_tarefas(id_usuario)
    return jsonify({"sucess": True, "tarefas": tarefas})

# 5. Concluir Tarefa
@instancia_processo_bp.route('/api/concluir-tarefa', methods=['POST'])
def api_concluir_tarefa():
    data = request.get_json()
    resultado = service.concluir_tarefa(
        id_tarefa=data.get('id_tarefa'),
        id_usuario=data.get('id_usuario'),
        texto_saida=data.get('texto_saida')
    )
    status_code = 200 if resultado.get('sucess') else 500
    return jsonify(resultado), status_code

# [NOVO] 6. Obter Timeline e Detalhes da Instância
@instancia_processo_bp.route('/api/instancia/<int:id_instancia>/timeline', methods=['GET'])
def api_get_timeline(id_instancia):
    # Pega o UID da Query String (ex: ?uid=1) para verificação de permissão
    uid = request.args.get('uid', 1, type=int)
    
    resultado = service.obter_detalhes_timeline(id_instancia, uid)
    
    status_code = 200 if resultado.get('sucess') else 404
    return jsonify(resultado), status_code