from flask import Flask, jsonify, request, send_from_directory
import jwt
import datetime

app = Flask(__name__)

# Chave secreta usada para assinar/verificar o token
SECRET_KEY = "mySecretKey"

@app.route("/")
def home():
    return send_from_directory(".", "index.html")

# Rota para gerar o token (válido por 1 hora)
@app.route("/gerar-token", methods=["GET"])
def gerar_token():
    payload = {
        "userId": 123,
        "username": "john_doe",
        "role": "admin",
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
    return jsonify({"token": token})

# Rota para verificar o token
@app.route("/verificar-token", methods=["POST"])
def verificar_token():
    data = request.get_json()
    token = data.get("token")

    try:
        decoded = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return jsonify({"mensagem": "Token válido!", "payload": decoded})
    except jwt.ExpiredSignatureError:
        return jsonify({"erro": "Token expirado!"}), 401
    except jwt.InvalidTokenError as e:
        return jsonify({"erro": "Token inválido!", "detalhes": str(e)}), 401

if __name__ == "__main__":
    app.run(debug=True)