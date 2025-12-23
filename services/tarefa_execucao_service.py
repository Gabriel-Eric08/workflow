from repositories.tarefa_execucao_repository import TarefaExecucaoRepository, db

class TarefaExecucaoService:
    def __init__(self):
        self.repo = TarefaExecucaoRepository()
    def create(self, id_instancia, id_etapa_definicao, id_funcionario, status_tarefa, texto_saida, data_conclusao):
        create = self.repo.create(id_instancia, id_etapa_definicao, id_funcionario, status_tarefa, texto_saida, data_conclusao)
        if create:
            db.session.commit()
            return True
        return False