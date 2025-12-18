from repositories.cargo_repository import CargoRepository, db

class CargoService:
    def __init__(self):
        self.repo = CargoRepository()
    
    def create_cargo(self, nome, descricao):
        if not nome or not descricao:
            return False
        validate= self.repo.create_cargo(nome,descricao)
        if validate:
            db.session.commit()
            return True
        return False