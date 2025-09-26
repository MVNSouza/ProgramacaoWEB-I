from http.server import BaseHTTPRequestHandler, HTTPServer

class SimpleHandler(BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, PATCH, OPTIONS, HEAD")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write("Requisição GET recebida com sucesso!".encode("utf-8"))

    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8")
        self.send_response(201)  # Created
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        resposta = f"Dados recebidos via POST: {body}"
        self.wfile.write(resposta.encode("utf-8"))

    def do_PUT(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8")
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        resposta = f"Dados recebidos via PUT: {body}"
        self.wfile.write(resposta.encode("utf-8"))

    def do_DELETE(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8")
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        resposta = f"Dados recebidos via DELETE: {body}"
        self.wfile.write(resposta.encode("utf-8"))

    def do_PATCH(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8")
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        resposta = f"Dados recebidos via PATCH: {body}"
        self.wfile.write(resposta.encode("utf-8"))

    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()

if __name__ == "__main__":
    httpd = HTTPServer(("localhost", 8080), SimpleHandler)
    print("Servidor rodando em http://localhost:8080")
    httpd.serve_forever()