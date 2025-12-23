from models.models import Funcionario, db

class FuncionarioRepository:
    def create_funcionario(self, id_cargo, nome, email, senha_hash, ativo):
       try:
        new_funcionario = Funcionario(
           id_cargo=id_cargo,
           nome=nome,
           email=email,
           senha_hash=senha_hash,
           ativo=ativo
        )
        db.session.add(new_funcionario)
        db.session.flush()
        return True
       except Exception as e:
          print(f"Repository error: {e}")
          return False
       
    def get_all(self):
       funcionarios = Funcionario.query.all()
       return funcionarios