from flask import Flask, jsonify, request

app = Flask(__name__)
produtos = [
        {"id": 1, "nome": "Notebook", "preco": 3500.00},
        {"id": 2, "nome": "Mouse", "preco": 80.00}
    ]

@app.route("/produtos", methods=["GET"])
def listar_produtos():
    
    return jsonify(produtos)

# Nova rota POST
@app.route("/produtos", methods=["POST"])
def adicionar_produto():
    dados = request.json
    produtos.append(dados)  # desserializa automaticamente
    return jsonify({"mensagem": "Produto recebido", "produto": dados}), 201

if __name__ == "__main__":
    app.run(debug=True)