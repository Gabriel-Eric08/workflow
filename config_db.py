from flask_sqlalchemy import SQLAlchemy

# Instancia o objeto do banco de dados (mas ainda não o conecta ao app)
db = SQLAlchemy()

class Config:
    """Configurações de conexão com o Banco de Dados"""
    # Credenciais: root:1234, Host: localhost, Porta: 3306, Banco: workflow
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:1234@localhost:3306/workflow'
    
    # Desativa rastreamento de modificações para economizar memória
    SQLALCHEMY_TRACK_MODIFICATIONS = False