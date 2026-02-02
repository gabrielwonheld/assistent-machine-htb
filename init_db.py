import logging
import os
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

from extensions import db
from models.userModel import User,Venda,Produto



logger = logging.getLogger(__name__)

def init_extensions(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
    return app

def init_app_db():
    """Cria o usuário administrador inicial se ele não existir."""
    from models.userModel import User # Import local para evitar erro circular
    
    try:
        if not User.query.filter_by(username="admin").first():
            admin = User(
                username=os.getenv("ADMIN_USERNAME", "admin"),
                is_admin=True
            )
            # Como o model usa password_hash, setamos diretamente ou usamos o método
            admin.set_password(os.getenv("ADMIN_PASSWORD", "adminpass"))
            
            db.session.add(admin)
            db.session.commit()
            print("✅ Banco inicializado e Admin criado.")
            
    except Exception as e:
        logger.error(f"❌ Erro crítico no seed: {e}")
        db.session.rollback()
        raise e