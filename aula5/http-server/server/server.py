import socket
from threading import Thread
from router import Router              # Roteador que sabe qual função executar
from .plumbing import Request, Response  # Interpreta requisições e monta respostas

class Server:
    def __init__(self):
        self.router = Router()  # Instancia o roteador

    def start(self, port=5000, host="", header_size=1024):
        """
        Inicia o servidor socket. Escuta conexões em uma porta definida.
        Cada conexão é tratada em uma thread separada.
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind((host, port))
            sock.listen(1)
            print(f"Servidor ouvindo em http://{socket.getfqdn()}:{port}/")

            while True:
                conn, addr = sock.accept()
                Thread(
                    target=self.handle_connection,
                    args=(conn, addr, header_size)
                ).start()

    def handle_connection(self, conn, addr, header_size):
        """
        Trata uma requisição recebida por socket.
        Interpreta os dados, encontra a rota e envia a resposta.
        """
        with conn:
            request_bytes = conn.recv(header_size)  # Lê a requisição (bruta)
            response = Response()                   # Prepara uma resposta vazia

            try:
                request = Request(request_bytes, addr)  # Constrói objeto da requisição
                self.router.handle_route(request, response)  # Executa rota
                print(f"{response.status_code} {request.method} {request.path}")
            except Exception as e:
                print("Erro ao processar a requisição:", e)
                response.status_code = 500
                response.body = "<h1>Erro interno no servidor</h1>"

            conn.sendall(response.serialize())  # Envia a resposta para o cliente

    def route(self, path, methods=None):
        """
        Decorador para registrar rotas como no Flask:
        @app.route("/caminho", methods=["GET"])
        """
        if methods is None:
            methods = ["GET"]
        return self.router.add_route(path, methods)
