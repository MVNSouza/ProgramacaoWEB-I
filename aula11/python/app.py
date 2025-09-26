from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/produtos", methods=["GET"])
def listar_produtos():
    produtos = [
        {"id": 1, "nome": "Notebook", "preco": 3500.00},
        {"id": 2, "nome": "Mouse", "preco": 80.00}
    ]
    return jsonify(produtos)

if __name__ == "__main__":
    app.run(debug=True)
