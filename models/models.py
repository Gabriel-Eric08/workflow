from datetime import datetime
from config_db import db # Importa a instância 'db' criada no app.py

class Cargo(db.Model):
    __tablename__ = 'cargos'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_cargo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(255))

    # Relacionamento: Um cargo tem vários funcionários
    funcionarios = db.relationship('Funcionario', backref='cargo', lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "nome_cargo": self.nome_cargo,
            "descricao": self.descricao
        }

    def __repr__(self):
        return f'<Cargo {self.nome_cargo}>'


class Funcionario(db.Model):
    __tablename__ = 'funcionarios'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_cargo = db.Column(db.Integer, db.ForeignKey('cargos.id'), nullable=False)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True)
    senha_hash = db.Column(db.Text)
    ativo = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {
            "id": self.id,             # ID do funcionário (não do cargo)
            "id_cargo": self.id_cargo, # ID do cargo vinculado
            "nome": self.nome,         # Nome da pessoa
            "email": self.email,       # Email
            "ativo": self.ativo        # Status
            # Dica de segurança: Evite retornar 'senha_hash' no JSON para o front-end
        }

    def __repr__(self):
        return f'<Funcionario {self.nome}>'


class ModeloProcesso(db.Model):
    __tablename__ = 'modelos_processos'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome_processo = db.Column(db.String(255), nullable=False)
    codigo_processo = db.Column(db.String(40), unique=True)
    descricao = db.Column(db.Text)

    # Relacionamento: Um modelo tem várias etapas e várias instâncias
    etapas = db.relationship('EtapaDefinicao', backref='modelo', lazy=True)
    instancias = db.relationship('InstanciaProcesso', backref='modelo', lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "nome_processo": self.nome_processo,    # Vamos usar as chaves em português
            "codigo_processo": self.codigo_processo, # para bater com sua rota register
            "descricao": self.descricao
        }


class EtapaDefinicao(db.Model):
    __tablename__ = 'etapas_definicao'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Colunas
    id_modelo = db.Column(db.Integer, db.ForeignKey('modelos_processos.id'), nullable=False)
    id_cargo = db.Column(db.Integer, db.ForeignKey('cargos.id'), nullable=False)
    
    nome_tarefa = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(255)) # Adicionei pois o HTML envia esse campo
    ordem_sequencial = db.Column(db.Integer, nullable=False)
    
    requer_anexo = db.Column(db.Boolean, default=False)
    requer_obs = db.Column(db.Boolean, default=False)
    
    # Relacionamento (para pegar o nome do cargo depois)
    cargo_responsavel = db.relationship('Cargo')

    def to_dict(self):
        return {
            "id": self.id,
            "id_modelo": self.id_modelo,
            "id_cargo": self.id_cargo,
            "nome_tarefa": self.nome_tarefa,
            "descricao": self.descricao,
            "ordem_sequencial": self.ordem_sequencial,
            "requer_anexo": self.requer_anexo,
            "requer_obs": self.requer_obs,
            
            # --- CORREÇÃO AQUI ABAIXO ---
            # Mudamos de .nome para .nome_cargo
            "nome_cargo": self.cargo_responsavel.nome_cargo if self.cargo_responsavel else "N/A"
        }

class InstanciaProcesso(db.Model):
    __tablename__ = 'instancias_processos'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_modelo = db.Column(db.Integer, db.ForeignKey('modelos_processos.id'), nullable=False)
    id_criador = db.Column(db.Integer, db.ForeignKey('funcionarios.id'))
    
    # Novo campo que adicionamos (MANTENHA ISSO)
    nome_processo = db.Column(db.String(255)) 
    
    data_inicio = db.Column(db.DateTime, default=datetime.utcnow)
    status_geral = db.Column(db.Integer, default=0) 

    criador = db.relationship('Funcionario')
    tarefas = db.relationship('TarefaExecucao', backref='instancia', lazy=True)


class TarefaExecucao(db.Model):
    __tablename__ = 'tarefas_execucao'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_instancia = db.Column(db.Integer, db.ForeignKey('instancias_processos.id'), nullable=False)
    id_etapa_definicao = db.Column(db.Integer, db.ForeignKey('etapas_definicao.id'))
    id_funcionario = db.Column(db.Integer, db.ForeignKey('funcionarios.id'))
    
    status_tarefa = db.Column(db.Integer, default=0) # 0: Pendente, 1: Concluido...
    texto_saida = db.Column(db.Text)
    data_conclusao = db.Column(db.DateTime)

    etapa_definicao = db.relationship('EtapaDefinicao')
    funcionario = db.relationship('Funcionario')
    anexos = db.relationship('AnexoTarefa', backref='tarefa', lazy=True)


class AnexoTarefa(db.Model):
    __tablename__ = 'anexos_tarefa'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_tarefa_executada = db.Column(db.Integer, db.ForeignKey('tarefas_execucao.id'), nullable=False)
    nome_arquivo = db.Column(db.String(255))
    url_arquivo = db.Column(db.Text)
    data_upload = db.Column(db.DateTime, default=datetime.utcnow)