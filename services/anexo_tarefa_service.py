from repositories.anexo_tarefa_repository import AnexoTarefaRepository, db

class AnexoTarefaService:
    def __init__(self):
        self.repo = AnexoTarefaRepository()
    def create(self,id_tarefa_executada, nome_arquivo,url_arquivo,data_upload):
        create = self.repo.create(id_tarefa_executada, nome_arquivo,url_arquivo,data_upload)
        if create:
            db.session.commit()
            return True
        return False