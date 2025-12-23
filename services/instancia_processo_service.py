from repositories.instancia_processo_repository import InstanciaProessoReository, db

class InstanciaProcessoService:
    def __init__(self):
        self.repo=InstanciaProessoReository()
    def create(self, id_modelo, id_criador, data_inicio, status_geral):
        if not id_modelo or not id_criador or not data_inicio or status_geral is None:
            return False
        create = self.repo.create(id_modelo, id_criador, data_inicio, status_geral)
        if create:
            db.session.commit()
            return True
        return False