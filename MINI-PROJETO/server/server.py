import socket
from threading import Thread
from .router import Router
from .plumbing import Request, Response


class Server:
    def __init__(self):
        self.router = Router()

    def start(self, port=5000, host="", buffer_size=1024):
        """
        Inicializa o servidor socket e aguarda conexões na porta especificada.
        Cada cliente é atendido em uma thread separada.
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind((host, port))
            server_socket.listen(1)

            print(f"Servidor rodando em http://localhost:{port}/")

            while True:
                client_conn, client_addr = server_socket.accept()
                Thread(
                    target=self.handle_connection,
                    args=(client_conn, client_addr, buffer_size)
                ).start()

    def handle_connection(self, conn, client_addr, buffer_size):
        """
        Processa a requisição de um cliente conectado.
        Interpreta os dados recebidos, encontra a rota correspondente
        e envia a resposta.
        """
        with conn:
            try:
                raw_request = conn.recv(buffer_size)
                request = Request(raw_request, client_addr)
                response = Response()

                self.router.handle_route(request, response)
                print(f"{response.status_code} {request.method} {request.path}")
            except Exception as err:
                print("Erro ao processar requisição:", err)
                response = Response(
                    body="<h1>Erro interno no servidor</h1>",
                    status_code=500
                )

            conn.sendall(response.serialize())

    def route(self, path, methods=None):
        """
        Decorador para registrar rotas, no estilo Flask:
        @app.route("/caminho", methods=["GET"])
        """
        allowed = methods or ["GET"]
        return self.router.add_route(path, allowed)
