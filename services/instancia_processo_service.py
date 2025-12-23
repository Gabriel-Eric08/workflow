from repositories.instancia_processo_repository import InstanciaProessoReository

class InstanciaProcessoService:
    def __init__(self):
        # Instancia o repositório (com o nome da classe mantido conforme solicitado)
        self.repo = InstanciaProessoReository()

    # 1. INICIAR UM NOVO PROCESSO
    def iniciar_processo(self, id_modelo, id_criador):
        # Validação básica
        if not id_modelo or not id_criador:
            return {"sucess": False, "message": "ID do Modelo e ID do Criador são obrigatórios."}
        
        # Chama o repositório. 
        # NOTA: Não precisa de db.session.commit() aqui, o repo já faz o controle de transação.
        return self.repo.iniciar_processo(id_modelo, id_criador)

    # 2. LISTAR MINHAS TAREFAS
    def get_minhas_tarefas(self, id_usuario):
        if not id_usuario:
            return []
        
        return self.repo.get_tarefas_pendentes(id_usuario)

    # 3. CONCLUIR TAREFA (TRAMITAR)
    def concluir_tarefa(self, id_tarefa, id_usuario, texto_saida=None):
        if not id_tarefa or not id_usuario:
            return {"sucess": False, "message": "Dados insuficientes para concluir a tarefa."}

        return self.repo.concluir_tarefa(id_tarefa, id_usuario, texto_saida)