from models.models import AnexoTarefa, db

class AnexoTarefaRepository:
    def create(self,id_tarefa_executada, nome_arquivo,url_arquivo,data_upload):
        try:
            novo_anexo_tarefa=AnexoTarefa(
                id_tarefa_executada=id_tarefa_executada,
                nome_arquivo=nome_arquivo,
                url_arquivo=url_arquivo,
                data_upload=data_upload
            )
            db.session.add(novo_anexo_tarefa)
            db.session.flush
            return True
        except Exception as e:
            print(f"Repository error: {e}")
            return False