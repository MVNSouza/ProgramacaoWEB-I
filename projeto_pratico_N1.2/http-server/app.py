from server import Server
from routes.usuarios import *

app = Server()

app.route("/usuarios")(listar_usuarios)
app.route("/usuarios/novo")(novo_usuario)
app.route("/usuarios", methods=["POST"])(criar_usuario)
app.route("/usuarios/(?P<id>\d+)")(detalhar_usuario)
app.route("/usuarios/(?P<id>\d+)/editar")(editar_usuario)
app.route("/usuarios/(?P<id>\d+)/atualizar", methods=["POST"])(atualizar_usuario)
app.route("/usuarios/(?P<id>\d+)/excluir", methods=["POST"])(excluir_usuario)

if __name__ == "__main__":
    app.start()
