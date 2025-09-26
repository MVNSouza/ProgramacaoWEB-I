import json, flask
import xml.etree.ElementTree as ET

app = flask.Flask(__name__)
clients = [
    {"nome": "alice", "idade": 30, "email": "alice@exemplo.com"},
    {"nome": "bob", "idade": 25, "email": "bob@exemplo.com"}
]
@app.route("/clientes", methods=["GET"])
def listar_clientes():
    if flask.request.headers.get("Accept") == "application/xml":
        xml = "<clientes>"
        for c in clients:
            xml += f"<cliente><nome>{c['nome']}</nome><idade>{c['idade']}</idade><email>{c['email']}</email></cliente>"
        xml += "</clientes>"
        return flask.Response(xml, mimetype="application/xml")
    return flask.jsonify(clients)


@app.route("/clientes", methods=["POST"])
def adicionar_cliente():
    if flask.request.headers.get("Content-Type""").startswith("application/xml"):

        tree = ET.fromstring(flask.request.data)
        nome = tree.findtext("nome")
        idade = int(tree.findtext("idade"))
        email = tree.findtext("email")

        cliente = {"nome": nome, "idade": idade, "email": email}
        clients.append(cliente)

        return flask.jsonify(cliente), 201
    return "Formato não suportado", 415

if __name__ == "__main__":
    app.run(debug=True)