from models.models import Cargo, db

class CargoRepository:
    def create_cargo(self, nome, descricao):
        try:
            novo_Cargo = Cargo(
                nome_cargo = nome,
                descricao = descricao
            )
            db.session.add(novo_Cargo)
            db.session.flush()
            return True
        except Exception as e:
            print(f"Repository error: {e}")
            return False
