from models.models import ModeloProcesso, db

class ModeloProcessoRepository:
    def create(self, nome_processo, codigo_processo, descricao):
        try:
            new_modelo_processo = ModeloProcesso(
                nome_processo=nome_processo,
                codigo_processo=codigo_processo,
                descricao=descricao
            )
            db.session.add(new_modelo_processo)
            db.session.flush()
            return True  
        except Exception as e:
            print(f"Repository error: {e}")
            return False