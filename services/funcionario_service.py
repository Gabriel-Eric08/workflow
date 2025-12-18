from repositories.funcionario_repository import FuncionarioRepository, db
import hashlib

class FuncionarioService:
    def __init__(self):
        self.repo = FuncionarioRepository()

    def create(self, id_cargo, nome, email, senha, ativo):
        if not id_cargo or not nome or not email or not senha or not ativo:
            return False
        senha_em_bytes = senha.encode('utf-8')
        hash_obj = hashlib.sha256(senha_em_bytes)
        hash_hex=hash_obj.hexdigest()
        created = self.repo.create_funcionario(id_cargo,nome,email,hash_hex,ativo)
        if created:
            db.session.commit()
            return True
        return False