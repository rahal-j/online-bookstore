from flask import Flask

def create_app():
    app = Flask(__name__)

    from .routes import notify_bp
    app.register_blueprint(notify_bp)

    return app
