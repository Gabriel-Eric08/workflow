from models.models import InstanciaProcesso,db

class InstanciaProessoReository:
    def create(self, id_modelo, id_criador, data_inicio, status_geral):
        try:
            nova_instancia = InstanciaProcesso(
                id_modelo=id_modelo,
                id_criador=id_criador,
                data_inicio=data_inicio,
                status_geral=status_geral
            )
            db.session.add(nova_instancia)
            db.session.flush()
            return True
        except Exception as e:
            print(f"Error in repository: {e}")
            return False