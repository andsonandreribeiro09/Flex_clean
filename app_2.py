from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func

app = Flask(__name__)

# Configuração do banco de dados PostgreSQL
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://seu_usuario:senha@localhost/seu_banco"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Modelos do Banco de Dados
class Cliente(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    telefone = db.Column(db.String(20), unique=True)
    endereco = db.Column(db.String(255))
    email = db.Column(db.String(255))

class Servico(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    descricao = db.Column(db.String(255))
    preco = db.Column(db.Numeric(10, 2), nullable=False)

class Funcionario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    cargo = db.Column(db.String(100))

class Agendamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    cliente_id = db.Column(db.Integer, db.ForeignKey("cliente.id"))
    servico_id = db.Column(db.Integer, db.ForeignKey("servico.id"))
    data = db.Column(db.Date, nullable=False)

class Pagamento(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    agendamento_id = db.Column(db.Integer, db.ForeignKey("agendamento.id"))
    valor = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.String(50), nullable=False)

class Estoque(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(255), nullable=False)
    quantidade = db.Column(db.Integer, nullable=False)
    unidade = db.Column(db.String(50))

# Rotas apenas para carregar os dados
def query_all(model):
    return jsonify([{col.name: getattr(row, col.name) for col in model.__table__.columns} for row in model.query.all()])

@app.route("/clientes")
def get_clientes():
    return query_all(Cliente)

@app.route("/servicos")
def get_servicos():
    return query_all(Servico)

@app.route("/funcionarios")
def get_funcionarios():
    return query_all(Funcionario)

@app.route("/agendamentos")
def get_agendamentos():
    return query_all(Agendamento)

@app.route("/pagamentos")
def get_pagamentos():
    return query_all(Pagamento)

@app.route("/estoque")
def get_estoque():
    return query_all(Estoque)

if __name__ == "__main__":
    app.run(debug=True)
