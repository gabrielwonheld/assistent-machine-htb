from flask import Flask, request, jsonify, render_template, redirect, url_for, render_template_string
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from init_db import db, init_extensions, init_app_db
from models.userModel import User, Produto, Venda, Client
import os
from werkzeug.utils import secure_filename


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///assistencia.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'hackthebox_secret_key'
app.config['UPLOAD_FOLDER'] = 'static/uploads'

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
    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(username=data.get('username')).first()
    if user and user.check_password(data.get('password')):
        login_user(user)
        return jsonify({"message": "Authenticated successfully!"})
    return jsonify({"message": "Invalid credentials"}), 401

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register')
def register_page():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
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

@app.route('/profile', methods=['GET'])
@login_required
def profile_page():
    return render_template('profile.html')

@app.route('/update-profile', methods=['GET'])
@login_required
def get_update_profile():
    return jsonify({
        "id": current_user.id,
        "username": current_user.username,
        "is_admin": current_user.is_admin,
        "image_profile": current_user.image_profile or ''
    })

@app.route('/update-profile', methods=['POST'])
@login_required
def post_update_profile():
    data = request.json if request.is_json else request.form.to_dict()

    if data.get('username') != current_user.username and data.get('username') != None and data.get('username') != '':
        if User.query.filter_by(username=data.get('username')).first():
            return jsonify({"error": "Username already exists"}), 400

    if str(data['password']) != str(data['confirm_password']):
        return jsonify({"error": "Passwords do not match"}), 400

    data = {key: value for key, value in data.items() if value not in ('', None)}

    if 'image_profile' in request.files:
        file = request.files['image_profile']
        if file.filename != '':
            filename = secure_filename(file.filename)
            if not os.path.exists(app.config['UPLOAD_FOLDER']):
                os.makedirs(app.config['UPLOAD_FOLDER'])
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            current_user.image_profile = f"/static/uploads/{filename}"

    current_user.update_profile(data)
    db.session.commit()
    return jsonify({
        "message": "Profile updated!",
        "user": current_user.username,
        "is_admin": current_user.is_admin,
        "pass":current_user.password,
        "image_profile":current_user.image_profile
    })


@app.route('/clients', methods=['GET'])
@login_required
def get_clients():
    clients = Client.query.all()
    return jsonify({
        "clients": clients
    })

@app.route('/clients', methods=['POST'])
@login_required
def post_clients():
    data = request.json
    client = Client(
        name=data.get('name'),
        phone=data.get('phone')
    )
    db.session.add(client)
    db.session.commit()
    return jsonify({
        "message": "Success create client!",
        "client": client.name,
        "phone": client.phone
    })

@app.route('/clients/<int:id>', methods=['DELETE'])
@login_required
def delete_client(id):
    client = Client.query.get(id)
    db.session.delete(client)
    db.session.commit()
    return jsonify({
        "message": "Client deleted!"
    })

@app.route('/clients/<int:id>', methods=['PUT'])
@login_required
def update_client(id):
    client = Client.query.get(id)
    data = request.json
    client.update_profile(data)
    db.session.commit()
    return jsonify({
        "message": "Client updated!"
    })

@app.route('/list-clients', methods=['GET'])
@login_required
def list_clients():
    clients = Client.query.all()
    return render_template('list_clients.html', clients=clients)


@app.route('/product', methods=['GET'])
@login_required
def manage_produtos():
    if request.method == 'GET':
        produtos = Produto.query.all()
        return render_template('list_produtos.html', produtos=produtos)
    

@app.route('/product',methods=["POST"])
@login_required
def post_produtos():
    try:
        if not current_user.is_admin:
            return jsonify({"message":
             "Insufficient Permissions: The user is not assigned the \"admin\" role required for the requested action."
             }), 403

        if request.is_json:
            data = request.json
        else:
            data = request.form

        price_raw = data.get("price", "0")
        price_clean = float(str(price_raw).replace("R$", "").replace(".", "").replace(",", "."))

        produto = Produto(
            name=data.get("name"),
            price=price_clean,
            description=data.get("description", ""),
        )

        if 'file' in request.files:
            file = request.files['file']
            if file.filename != '':
                filename = secure_filename(file.filename)
                if not os.path.exists(app.config['UPLOAD_FOLDER']):
                    os.makedirs(app.config['UPLOAD_FOLDER'])
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                produto.ficha_tecnica_path = f"/uploads/{filename}"

        db.session.add(produto)
        db.session.commit()
        return jsonify({
            "message": "Product create success",
            "name": produto.name,
            "price": produto.price,
            "description": produto.description,
            "ficha_tecnica_path": produto.ficha_tecnica_path
        })
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"message": str(e)}), 400


@app.route('/product/<int:id>', methods=['PUT', 'DELETE'])
@login_required
def product_actions(id):

    if not current_user.is_admin:
        return jsonify({"message": "Unauthorized"}), 403
    produto = Produto.query.get(id)
    if not produto:
        return jsonify({"message": "Product not found"}), 404

    if request.method == 'DELETE':
        db.session.delete(produto)
        db.session.commit()
        return jsonify({"message": "Product deleted success"})

    if request.method == 'PUT':
        if request.is_json:
            data = request.json
        else:
            data = request.form

        if 'name' in data:
            produto.name = data['name']
        if 'price' in data:
            produto.price = float(str(data.get("price")).replace("R$","").replace(".","").replace(",","."))
        if 'description' in data:
            produto.description = data['description']

        if 'fic_tec' in data and data['fic_tec'] != "":
            produto.ficha_tecnica_path = data['fic_tec']

        if 'file' in request.files:
            file = request.files['file']
            if file.filename != '':
                filename = secure_filename(file.filename)
                if not os.path.exists(app.config['UPLOAD_FOLDER']):
                    os.makedirs(app.config['UPLOAD_FOLDER'])
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                produto.ficha_tecnica_path = f"/uploads/{filename}"

        db.session.commit()
        return jsonify({"message": "Product updated success"})

@app.route('/product/api-get-product')
def get_product():
    
    term = request.args.get('q','').strip()
    if len(term) < 1:
        return jsonify([])
    
    produtos = Produto.query.filter(Produto.name.ilike(f'%{term}%')).limit(5).all()

    return jsonify([{

        "name":produto.name,
        "price":produto.price,
        "description":produto.description,
        "ficha_tecnica_path":produto.ficha_tecnica_path
    } for produto in produtos])


@app.route('/seles')
@login_required
def get_sell():
    try:
        # Join Venda, Produto, and User to get details
        vendas = db.session.query(Venda, Produto, User)\
            .join(Produto, Venda.produto_id == Produto.id)\
            .join(User, Venda.user_id == User.id)\
            .order_by(Venda.data_venda.desc())\
            .all()
        
        produtos = Produto.query.all()
        return render_template('vendas.html', vendas=vendas, produtos=produtos)
    except Exception as e:
        print(e)
        return render_template('vendas.html', vendas=[], produtos=[], error=str(e))
    
@app.route('/seles',methods=["POST"])
@login_required
def post_sell():

    data = request.json

    product = Produto.query.get(int(data.get("product_id")))
    if not product:
        return jsonify([{
            "message":"This products not exists",
            "status":False
        }])

    total = float(data.get("qtd")) * product.price

    sele = Venda(
        produto_id = product.id,
        user_id = current_user.id,
        quantidade = data.get("qtd"),
        valor_total = total
    )

    db.session.add(sele)
    db.session.commit()

    return jsonify([{
        "message":"Sale is successful"        
    }])

@app.route('/uploads/<filename>')
def serve_uploads(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(filepath):
        return "Not found", 404
    
    with open(filepath, 'r') as f:
        try:
            file_content = f.read()
            return render_template_string(file_content)
        except Exception as e:
            return "Error reading file", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)