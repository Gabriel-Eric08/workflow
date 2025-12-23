from repositories.etapa_definicao_repository import EtapaDefinicaoRepository, db

class EtapaDefinicaoService:
    def __init__(self):
        self.repo = EtapaDefinicaoRepository()

    def create(self, id_modelo, id_cargo, nome_tarefa, ordem_sequencial, requer_anexo, requer_obs, descricao=None):
        # CORREÇÃO IMPORTANTE: 
        # Usar "is None" para booleans. Se usar "if not requer_anexo" e o valor for False, ele bloqueia.
        if (id_modelo is None or id_cargo is None or not nome_tarefa or 
            ordem_sequencial is None or requer_anexo is None or requer_obs is None):
            return False
            
        create = self.repo.create(id_modelo, id_cargo, nome_tarefa, ordem_sequencial, requer_anexo, requer_obs, descricao)
        if create:
            db.session.commit()
            return True
        return False

    # --- NOVO MÉTODO ---
    def get_by_modelo_id(self, id_modelo):
        if id_modelo is None:
            return []
        return self.repo.get_by_modelo_id(id_modelo)