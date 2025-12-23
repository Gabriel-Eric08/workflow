from flask import Flask
from config_db import db, Config
from routes.cargo import cargo_bp # Importa o blueprint
from routes.funcionario import funcionario_bp
from routes.etapa_definicao import etapa_definicao_bp
from routes.modelo_processo import modelo_processo_bp
from routes.instancia_processo import instancia_processo_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    app.register_blueprint(cargo_bp, url_prefix='/cargo')
    app.register_blueprint(funcionario_bp, url_prefix='/funcionario')
    app.register_blueprint(etapa_definicao_bp, url_prefix='/etapa/definicao')
    app.register_blueprint(modelo_processo_bp, url_prefix='/modelo/processo')
    app.register_blueprint(instancia_processo_bp, url_prefix='/instancia/processo')
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5050)