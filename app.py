from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Habilita CORS para permitir que outros domínios acessem sua API

# Usando a Connection URL fornecida sem senha
# app.config['SQLALCHEMY_DATABASE_URI']= 'mysql://root:tccDxwLofJMQyuvBcbZMSJMQtLSWNVib@autorack.proxy.rlwy.net:35115/railway'
app.config['SQLALCHEMY_DATABASE_URI']= 'mysql+mysqlconnector://root:tccDxwLofJMQyuvBcbZMSJMQtLSWNVib@autorack.proxy.rlwy.net:35115/railway'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Definindo o modelo
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    mensagem = db.Column(db.String(200), nullable=False)

# Criação das tabelas
with app.app_context():
    db.create_all()

# Endpoint para adicionar um usuário
@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.json

    # Validação básica dos dados
    if not data or not all(key in data for key in ('name', 'email', 'mensagem')):
        return jsonify({'error': 'Dados incompletos'}), 400

    try:
        # Criação de uma nova instância de User
        new_user = User(
            name=data['name'],
            email=data['email'],
            mensagem=data['mensagem']
        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'Usuário adicionado com sucesso!'}), 201

    except Exception as e:
        # Captura qualquer exceção e reverte a sessão para evitar transações incompletas
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
