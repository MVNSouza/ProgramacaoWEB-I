import socket
from threading import Thread
from .router import Router         # Importação absoluta (melhor para rodar direto)
from .plumbing import Request, Response

class Server:
    def __init__(self):
        self.router = Router()
        self.host = '127.0.0.1'
        self.port = 5000

    def start(self, host=None, port=None):
        self.host = host or self.host
        self.port = port or self.port
        
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind((self.host, self.port))
            sock.listen(5)
            print(f"🚀 Servidor rodando em http://{self.host}:{self.port}/usuarios")

            while True:
                conn, addr = sock.accept()
                Thread(
                    target=self.handle_connection,
                    args=(conn,),
                    daemon=True
                ).start()

    def handle_connection(self, conn):
        with conn:
            try:
                request_data = conn.recv(1024)
                if not request_data:
                    return

                request = Request(request_data)
                response = Response()

                self.router.handle_route(request, response)

                conn.sendall(response.serialize())
                print(f"{response.status_code} {request.method} {request.path}")

            except Exception as e:
                print(f"Erro na conexão: {e}")
                error_resp = Response()
                error_resp.status_code = 500
                error_resp.body = "<h1>500 Internal Server Error</h1>"
                error_resp.headers['Content-Type'] = 'text/html'
                conn.sendall(error_resp.serialize())

    def route(self, path, methods=None):
        return self.router.add_route(path, methods)
