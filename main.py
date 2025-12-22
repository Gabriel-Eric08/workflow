from flask import Flask
from config_db import db, Config
from routes.cargo import cargo_bp # Importa o blueprint
from routes.funcionario import funcionario_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    app.register_blueprint(cargo_bp, url_prefix='/cargo')
    app.register_blueprint(funcionario_bp, url_prefix='/funcionario')
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5050)