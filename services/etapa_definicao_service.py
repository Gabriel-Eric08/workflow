from repositories.etapa_definicao_repository import EtapaDefinicaoRepository, db

class EtapaDefinicaoService:
    def __init__(self):
        self.repo= EtapaDefinicaoRepository()
    def create(self, id_modelo, id_cargo, nome_tarefa, ordem_sequencial, requer_anexo, requer_obs):
        if not id_modelo or not id_cargo or not nome_tarefa or not ordem_sequencial or not requer_anexo or not requer_obs:
            return False
        create = self.repo.create(id_modelo, id_cargo, nome_tarefa, ordem_sequencial, requer_anexo, requer_obs)
        if create:
            db.session.commit()
            return True
        return False