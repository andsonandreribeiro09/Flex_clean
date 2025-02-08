from flask import Flask, jsonify, request, render_template
import pandas as pd
import os

app = Flask(__name__)

# Caminhos dos arquivos CSV
CLIENTES_CSV = "clientes.csv"
SERVICOS_CSV = "servicos.csv"
FUNCIONARIOS_CSV = "funcionarios.csv"
AGENDAMENTOS_CSV = "agendamentos.csv"
PAGAMENTOS_CSV = "pagamentos.csv"
ESTOQUE_CSV = "estoque.csv"

# Função para carregar os dados com tratamento
def carregar_dados():
    global clientes, servicos, funcionarios, agendamentos, pagamentos, estoque

    def carregar_csv(arquivo, colunas_tipos=None):
        if os.path.exists(arquivo):
            df = pd.read_csv(arquivo).fillna("")  # Preenche NaN com string vazia
            if colunas_tipos:
                for coluna, tipo in colunas_tipos.items():
                    df[coluna] = df[coluna].astype(tipo, errors="ignore")  # Converte sem quebrar o código
            return df.to_dict(orient="records")
        return []  # Retorna lista vazia se o arquivo não existir

    # Carregar arquivos com tipos definidos
    clientes = carregar_csv(CLIENTES_CSV, {"ID": int})
    servicos = carregar_csv(SERVICOS_CSV, {"ID": int, "Preço": float})
    funcionarios = carregar_csv(FUNCIONARIOS_CSV, {"ID": int})
    agendamentos = carregar_csv(AGENDAMENTOS_CSV, {"ID": int, "Cliente_ID": int, "Funcionario_ID": int, "Serviço_ID": int})
    pagamentos = carregar_csv(PAGAMENTOS_CSV, {"ID": int, "Cliente_ID": int, "Valor": float})
    estoque = carregar_csv(ESTOQUE_CSV, {"ID": int})

# Carregar dados ao iniciar
carregar_dados()


@app.route("/")
def index():
    return render_template("index.html", clientes=clientes, servicos=servicos, funcionarios=funcionarios, agendamentos=agendamentos, pagamentos=pagamentos, estoque=estoque)

@app.route("/clientes", methods=["GET", "POST"])
def manage_clientes():
    if request.method == "POST":
        novo_cliente = request.json
        clientes.append(novo_cliente)
        pd.DataFrame(clientes).to_csv(CLIENTES_CSV, index=False, encoding="utf-8")
        return jsonify({"message": "Cliente adicionado!"}), 201
    return jsonify(clientes)

@app.route("/servicos", methods=["GET", "POST"])
def manage_servicos():
    if request.method == "POST":
        novo_servico = request.json
        servicos.append(novo_servico)
        pd.DataFrame(servicos).to_csv(SERVICOS_CSV, index=False, encoding="utf-8")
        return jsonify({"message": "Serviço adicionado!"}), 201
    return jsonify(servicos)

@app.route("/funcionarios", methods=["GET", "POST"])
def manage_funcionarios():
    if request.method == "POST":
        novo_funcionario = request.json
        funcionarios.append(novo_funcionario)
        pd.DataFrame(funcionarios).to_csv(FUNCIONARIOS_CSV, index=False, encoding="utf-8")
        return jsonify({"message": "Funcionário adicionado!"}), 201
    return jsonify(funcionarios)

@app.route("/agendamentos", methods=["GET", "POST"])
def manage_agendamentos():
    if request.method == "POST":
        novo_agendamento = request.json
        agendamentos.append(novo_agendamento)
        pd.DataFrame(agendamentos).to_csv(AGENDAMENTOS_CSV, index=False, encoding="utf-8")
        return jsonify({"message": "Agendamento adicionado!"}), 201
    return jsonify(agendamentos)

@app.route("/pagamentos", methods=["GET", "POST"])
def manage_pagamentos():
    if request.method == "POST":
        novo_pagamento = request.json
        pagamentos.append(novo_pagamento)
        pd.DataFrame(pagamentos).to_csv(PAGAMENTOS_CSV, index=False, encoding="utf-8")
        return jsonify({"message": "Pagamento adicionado!"}), 201
    return jsonify(pagamentos)

@app.route("/estoque", methods=["GET", "POST"])
def manage_estoque():
    if request.method == "POST":
        novo_produto = request.json
        estoque.append(novo_produto)
        pd.DataFrame(estoque).to_csv(ESTOQUE_CSV, index=False, encoding="utf-8")
        return jsonify({"message": "Produto adicionado ao estoque!"}), 201
    return jsonify(estoque)


@app.route("/dashboard")
def dashboard():
    
    dados = {
        "ordens_servico_hoje": len([a for a in agendamentos if a.get("Data") == "2025-02-08"]),
        "vendas_hoje": len([p for p in pagamentos if p.get("Data") == "2025-02-08"]),
        "receitas_hoje": sum(float(p.get("Valor", 0)) for p in pagamentos if p.get("Data") == "2025-02-08"),
        "clientes_reembolsados": sum(1 for p in pagamentos if p.get("Status") == "Reembolsado"),
        "recebiveis": sum(float(p.get("Valor", 0)) for p in pagamentos if p.get("Status") == "Pendente"),
        "dinheiro_total": sum(float(p.get("Valor", 0)) for p in pagamentos),
        "ordens_pendentes": len([a for a in agendamentos if a.get("Status") == "Pendente"]),
        "ordens_urgentes": len([a for a in agendamentos if a.get("Prioridade") == "Urgente"]),
        "ordens_atrasadas": len([a for a in agendamentos if a.get("Status") == "Atrasado"]),
    }
    return render_template("index.html", dados=dados)

@app.route("/dashboard-dados")
def dashboard_dados():
    # Simulação de dados dinâmicos (substitua pelos seus cálculos)
    dados = {
        "ordens_servico": 10,
        "vendas": 5,
        "receita": 1500.00,
        "reembolsos": 200.00,
        "ordens_pendentes": 2,
        "ordens_urgentes": 1,
        "valor_medio_venda": 300.00
    }
    return jsonify(dados)

@app.route("/adicionar", methods=["POST"])
def adicionar_dado():
    novo_dado = request.json

    if novo_dado:
        global clientes  # Altere conforme a tabela que está sendo editada
        clientes.append(novo_dado)
        pd.DataFrame(clientes).to_csv(CLIENTES_CSV, index=False, encoding="utf-8")
        return jsonify({"message": "Dado adicionado com sucesso!"}), 201
    return jsonify({"message": "Erro ao adicionar"}), 400


if __name__ == "__main__":
    app.run(debug=True)