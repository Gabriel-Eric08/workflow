from repositories.instancia_processo_repository import InstanciaProcessoReository

class InstanciaProcessoService:
    def __init__(self):
        self.repo = InstanciaProcessoReository()

    # Iniciar
    def iniciar_processo(self, id_modelo, id_criador):
        if not id_modelo or not id_criador:
            return {"sucess": False, "message": "Dados obrigatórios faltando."}
        return self.repo.iniciar_processo(id_modelo, id_criador)

    # Listar TODAS (Dashboard Direita)
    def get_todas_instancias(self):
        return self.repo.get_todas_instancias()

    # Listar APENAS MODELOS (Dashboard Esquerda - Dropdown)
    def get_modelos_dropdown(self):
        modelos = self.repo.get_lista_modelos_simples()
        # Formatar para lista de dicionários simples
        return [{"id": m.id, "nome": m.nome_processo} for m in modelos]

    # Listar Tarefas (Minha Caixa de Entrada)
    def get_minhas_tarefas(self, id_usuario):
        if not id_usuario: return []
        return self.repo.get_tarefas_pendentes(id_usuario)

    # Concluir
    def concluir_tarefa(self, id_tarefa, id_usuario, texto_saida=None):
        return self.repo.concluir_tarefa(id_tarefa, id_usuario, texto_saida)
    def obter_detalhes_timeline(self, id_instancia, id_usuario_visualizador):
        """
        Monta a estrutura completa da timeline e decide se o usuário
        atual pode executar a tarefa pendente.
        """
        # 1. Busca Instância
        instancia = self.repo.get_instancia_por_id(id_instancia)
        if not instancia:
            return {"sucess": False, "message": "Instância não encontrada"}

        # 2. Busca Usuário para saber o cargo dele (Lógica de Permissão)
        usuario_logado = self.repo.get_usuario_por_id(id_usuario_visualizador)
        id_cargo_usuario = usuario_logado.id_cargo if usuario_logado else -1

        # 3. Busca Tarefas Brutas
        tarefas_brutas = self.repo.get_timeline_tarefas(id_instancia)

        # 4. Formata os dados para o Frontend
        timeline_formatada = []
        
        for tarefa, etapa, func in tarefas_brutas:
            # Lógica: O usuário pode executar SE a tarefa estiver pendente (0)
            # E o cargo da etapa for igual ao cargo do usuário.
            pode_executar_essa = (
                tarefa.status_tarefa == 0 and 
                etapa.id_cargo == id_cargo_usuario
            )

            item = {
                "id_tarefa": tarefa.id,
                "nome_tarefa": etapa.nome_tarefa,
                "descricao": etapa.descricao,
                "status": tarefa.status_tarefa, # 0 ou 1
                "responsavel_nome": func.nome if func else None,
                
                # Dados de permissão e UI
                "nome_cargo_etapa": etapa.cargo_responsavel.nome_cargo, # SQLAlchemy relationship
                "pode_executar": pode_executar_essa, 
                
                "data_conclusao": tarefa.data_conclusao.strftime('%d/%m/%Y %H:%M') if tarefa.data_conclusao else None,
                "texto_saida": tarefa.texto_saida,
                "requer_obs": etapa.requer_obs
            }
            timeline_formatada.append(item)

        return {
            "sucess": True,
            "instancia": {
                "id": instancia.id,
                "nome_processo": instancia.nome_processo,
                "status_geral": instancia.status_geral,
                "data_inicio": instancia.data_inicio.strftime('%d/%m/%Y')
            },
            "timeline": timeline_formatada
        }