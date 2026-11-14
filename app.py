import os
from datetime import datetime
from flask import Flask, render_template, jsonify
from sqlalchemy import text
from config import Config
from extensions import db, migrate, csrf
from models import Setting


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app)

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    from routes import main_bp
    from admin_routes import admin_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')

    @app.context_processor
    def inject_settings():
        try:
            settings = Setting.query.first()
        except Exception:
            settings = None
        return dict(site_settings=settings, current_year=datetime.now().year)

    @app.get("/healthz")
    def healthz():
        """Diagnostic endpoint: checks whether the app can reach TiDB."""
        try:
            db.session.execute(text("SELECT 1"))
            return jsonify(status="ok", database="connected"), 200
        except Exception:
            app.logger.exception("Database health check failed")
            db.session.rollback()
            return jsonify(status="error", database="unavailable"), 503

    @app.errorhandler(404)
    def not_found(e):
        return render_template('404.html'), 404

    return app


app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
