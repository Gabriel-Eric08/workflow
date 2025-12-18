from flask import Flask
from config_db import db, Config

# Aqui você importará apenas os Blueprints (Rotas/Controllers)
# from controllers.processo_controller import processo_bp 

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    with app.app_context():
        return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=6000)