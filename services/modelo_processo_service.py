from repositories.modelo_processo_repsitory import ModeloProcessoRepository,db

class ModeloProcessoService:
    def __init__(self):
        self.repo = ModeloProcessoRepository()
    def create(self, nome_processo, codigo_processo, descricao):
        if not nome_processo or not codigo_processo or not descricao:
            return False
        create = self.repo.create(nome_processo,codigo_processo,descricao)
        if create:
            db.session.commit()
            return True
        return False