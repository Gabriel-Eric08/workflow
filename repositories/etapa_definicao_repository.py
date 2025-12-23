from models.models import EtapaDefinicao, db

class EtapaDefinicaoRepository:
    
    def create(self, id_modelo, id_cargo, nome_tarefa, ordem_sequencial, requer_anexo, requer_obs, descricao=None):
        try:
            nova_etapa = EtapaDefinicao(
                id_modelo=id_modelo,
                id_cargo=id_cargo,
                nome_tarefa=nome_tarefa,
                descricao=descricao,  # Adicionado
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

    # --- NOVO MÉTODO NECESSÁRIO PARA O FRONT-END ---
    def get_by_modelo_id(self, id_modelo):
        try:
            # Busca todas as etapas daquele modelo, ordenadas pela sequência (1, 2, 3...)
            return EtapaDefinicao.query.filter_by(id_modelo=id_modelo)\
                .order_by(EtapaDefinicao.ordem_sequencial.asc())\
                .all()
        except Exception as e:
            import traceback
            traceback.print_exc()  # <--- ISSO VAI MOSTRAR O ERRO COMPLETO NO TERMINAL
            print(f"Error getting etapas: {e}")
            return []