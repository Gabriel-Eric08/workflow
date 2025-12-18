from models import Cargo, db

class CargoRepository:
    def create_cargo(nome, descricao):
        novo_Cargo = Cargo(
            nome,
            descricao
        )
        db.session.add(novo_Cargo)
        db.session.flush()
        return True