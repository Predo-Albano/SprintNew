import os
from flask import Flask, redirect, url_for
from config import SECRET_KEY, SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS
from database import db
from routes.usuario_routes import usuario_bp
from routes.agendamento_routes import agendamento_bp
from routes.admin_routes import admin_bp
from chatbot import chatbot_bp

app = Flask(__name__, static_folder='static')
#app = Flask(__name__)

# Configurações do aplicativo
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS

# Inicializa o banco de dados
db.init_app(app)

# Registra os blueprints
app.register_blueprint(usuario_bp)
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(agendamento_bp)
app.register_blueprint(chatbot_bp)  # Registra o chatbot no Flask


# Cria as tabelas do banco de dados (se não existirem)
with app.app_context():
    db.create_all()

# Rota inicial (redireciona para o login)
@app.route('/')
def index():
    return redirect(url_for('usuario.login'))

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Obtém a porta da variável de ambiente ou usa 5000
    app.run(debug=True, host='0.0.0.0', port=port)  # Executa o servidor
