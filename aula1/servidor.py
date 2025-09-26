from http.server import BaseHTTPRequestHandler, HTTPServer

class MyRequestHandler(BaseHTTPRequestHandler):

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header(
            "Access-Control-Allow-Methods",
            "GET, POST, PUT, DELETE, PATCH, OPTIONS, HEAD"
        )
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    # GET
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write("GET recebido com sucesso!".encode("utf-8"))

    # HEAD
    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()

    # Função interna para ler corpo das requisições
    def _ler_corpo(self):
        tamanho = int(self.headers.get("Content-Length", 0))
        return self.rfile.read(tamanho).decode("utf-8")

    # POST
    def do_POST(self):
        corpo = self._ler_corpo()
        self.send_response(201)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(f"POST recebido: {corpo}".encode("utf-8"))

    # PUT
    def do_PUT(self):
        corpo = self._ler_corpo()
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(f"PUT recebido: {corpo}".encode("utf-8"))

    # DELETE
    def do_DELETE(self):
        corpo = self._ler_corpo()
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(f"DELETE recebido: {corpo}".encode("utf-8"))

    # PATCH
    def do_PATCH(self):
        corpo = self._ler_corpo()
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(f"PATCH recebido: {corpo}".encode("utf-8"))

if __name__ == "__main__":
    servidor = HTTPServer(("localhost", 8080), MyRequestHandler)
    print("Servidor rodando em http://localhost:8080")
    servidor.serve_forever()
