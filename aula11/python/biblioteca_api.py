from flask import Flask, request, jsonify, Response

app = Flask(__name__)

# Lista de livros inicial
biblioteca = [
    {"id": 1, "titulo": "1984" , "autor": "George Orwell", "ano": 1949},
    {"id": 2, "titulo": "O Senhor dos Anéis", "autor": "J.R.R. Tolkien", "ano": 1954}
]

# Endpoint GET com suporte a JSON e XML
@app.route("/livros", methods=["GET"])
def listar_livros():
    if request.headers.get("Accept") == "application/xml":
        xml = "<biblioteca>"
        for p in biblioteca:
            xml += f"<biblioteca><id>{p['id']}</id><titulo>{p['titulo']}</titulo><autor>{p['autor']}</autor><ano>{p["ano"]}</ano></biblioteca>"
        xml += "</produtos>"
        return Response(xml, mimetype="application/xml")
    return jsonify(biblioteca)

# Endpoint POST para adicionar livros em JSON
@app.route("/livros", methods=["POST"])
def adicionar_produto():
    dados = request.json  # desserialização automática
    biblioteca.append(dados)
    return jsonify({"mensagem": "Produto adicionado com sucesso", "produto": dados}), 201

if __name__ == "__main__":
    app.run(debug=True)