from flask import Flask, jsonify, request

app = Flask(__name__)
users = [{"id": 1, "nome": "Alice", "email": "alice@exemplo.com", "cursos" : ["pw1", 'bd', 'lp1']},
          {"id": 2, "nome": "Bob", "email": "bob@exemplo.com","cursos" : ["pw1", 'bd', 'lp1']}
]

@app.route("/usuarios", methods=["GET"])
def listar_usuarios():
    return jsonify(users)

@app.route("/usuarios", methods=["POST"])
def add_usuario():
    dados = request.json
    users.append(dados)
    return jsonify({"mensagem": "Usuário adicionado", "usuario": dados}), 201   

if __name__ == "__main__":
    app.run(debug=True)