from flask import Flask, request, jsonify
from flask_login import LoginManager, login_user, login_required, current_user
from init_db import db, init_extensions, init_app_db
from models.userModel import User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///assistencia.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'hackthebox_secret_key'

# 1. Inicializa o banco e cria tabelas
init_extensions(app)

# 2. Roda o seed de dados dentro do contexto
with app.app_context():
    init_app_db()

# 3. Configura o Login
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- ROTAS ---

@app.route('/')
def index():
    return jsonify({"status": "online", "message": "Sistema de Assistência Técnica v1.0"})

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data.get('username')).first()
    if user and user.check_password(data.get('password')):
        login_user(user)
        return jsonify({"message": "Autenticado com sucesso!"})
    return jsonify({"message": "Credenciais inválidas"}), 401

@app.route('/register', methods=['POST'])
# @login_required
def register_profile():

    data = request.json
    user = User(
        username=data.get('username'),
        is_admin=False
    )
    user.set_password(data.get('password'))
    db.session.add(user)
    db.session.commit()
    return jsonify({
        "message": "Success create user!",
        "user": user.username,
        "is_admin": user.is_admin
    })

@app.route('/update-profile', methods=['GET'])
@login_required
def get_update_profile():
    return jsonify({
        "id": current_user.id,
        "username": current_user.username,
        "is_admin": current_user.is_admin
        # "role": "operador" if not current_user.is_admin else "admin"
    })

@app.route('/update-profile', methods=['POST'])
@login_required
def post_update_profile():
    data = request.json
    # O Mass Assignment acontece aqui
    current_user.update_profile(data)
    db.session.commit()
    return jsonify({
        "message": "Perfil atualizado!",
        "user": current_user.username,
        "is_admin": current_user.is_admin
    })

# Rota de teste para verificar se é admin
@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        return jsonify({"error": "Acesso negado. Apenas administradores."}), 403
    return jsonify({"message": "Bem-vindo à área restrita, Admin!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)