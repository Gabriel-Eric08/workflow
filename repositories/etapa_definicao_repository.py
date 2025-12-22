from models.models import EtapaDefinicao, db

class EtapaDefinicaoRepository:
    def create(self, id_modelo, id_cargo, nome_tarefa, ordem_sequencial, requer_anexo, requer_obs):
        try:
            nova_etapa = EtapaDefinicao(
                id_modelo=id_modelo,
                id_cargo=id_cargo,
                nome_tarefa=nome_tarefa,
                ordem_sequencial=ordem_sequencial,
                requer_anexo=requer_anexo,
                requer_obs=requer_obs
            )
            db.session.add(nova_etapa)
            db.session.flush()
            return True
        except Exception as e:
            print(f"Error in repository: {e}")
            return False