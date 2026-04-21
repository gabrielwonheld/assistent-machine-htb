import logging
import os
# from flask_sqlalchemy import SQLAlchemy
# from werkzeug.security import generate_password_hash

from extensions import db
from models.userModel import User,Produto,Client



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
            
        list_produtos = [
            {
                "name": "Wireless Router",
                "price": 10.0,
                "description": "Wireless Router",
                "ficha_tecnica_path": "/uploads/ficha_tecnica_1.html"
            },
            {
                "name": "keyboard",
                "price": 20.0,
                "description": "keyboard",
                "ficha_tecnica_path": "/uploads/ficha_tecnica_2.html"
            },
            {
                "name": "mouse",
                "price": 30.0,
                "description": "mouse",
                "ficha_tecnica_path": "/uploads/ficha_tecnica_3.html"
            },
            {
                "name": "monitor",
                "price": 30.0,
                "description": "monitor",
                "ficha_tecnica_path": "/uploads/ficha_tecnica_4.html"
            },
            {
                "name": "notebook",
                "price": 30.0,
                "description": "notebook",
                "ficha_tecnica_path": "/uploads/ficha_tecnica_5.html"
            },
            {
                "name": "headset",
                "price": 30.0,
                "description": "headset",
                "ficha_tecnica_path": "/uploads/ficha_tecnica_6.html"
            },
            {
                "name": "webcam",
                "price": 30.0,
                "description": "webcam",
                "ficha_tecnica_path": "/uploads/ficha_tecnica_7.html"
            }
        ]
        
        for produto in list_produtos:
            db.session.add(Produto(**produto))


        list_clients = [
            {
                "name": "Joshua",
                "phone": "63928273588",
            },
            {
                "name": "Pedro",
                "phone": "8435672693",
            },
            {
                "name": "Maria",
                "phone": "6839123419",
            },
            {
                "name": "Ana",
                "phone": "6455555555",
            },
            {
                "name": "Carlos",
                "phone": "6821879177",
            },
            {
                "name": "Fernanda",
                "phone": "9236527718",
            },
            {
                "name": "Rafael",
                "phone": "7930347778",
            },
            {
                "name": "Juliana",
                "phone": "6824124173",
            },
            {
                "name": "Lucas",
                "phone": "9834133628",
            },
            {
                "name": "Mariana",
                "phone": "7324701387",
            }
        ]

        for client in list_clients:
            db.session.add(Client(**client))

        db.session.commit()
        print("✅ Banco inicializado e Admin criado.")
            
    except Exception as e:
        logger.error(f"❌ Erro crítico no seed: {e}")
        db.session.rollback()
        raise e