from flask import Flask, request, jsonify, Response

app = Flask(__name__)

# Lista de produtos inicial
produtos = [
    {"id": 1, "nome": "Notebook", "preco": 3500.00},
    {"id": 2, "nome": "Mouse", "preco": 80.00}
]

# Endpoint GET com suporte a JSON e XML
@app.route("/produtos", methods=["GET"])
def listar_produtos():
    if request.headers.get("Accept") == "application/xml":
        xml = "<produtos>"
        for p in produtos:
            xml += f"<produto><id>{p['id']}</id><nome>{p['nome']}</nome><preco>{p['preco']}</preco></produto>"
        xml += "</produtos>"
        return Response(xml, mimetype="application/xml")
    return jsonify(produtos)

# Endpoint POST para adicionar produtos em JSON
@app.route("/produtos", methods=["POST"])
def adicionar_produto():
    dados = request.json  # desserialização automática
    produtos.append(dados)
    return jsonify({"mensagem": "Produto adicionado com sucesso", "produto": dados}), 201

if __name__ == "__main__":
    app.run(debug=True)