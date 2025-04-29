from http.server import BaseHTTPRequestHandler, HTTPServer

class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write("Olá, mundo!".encode("utf-8"))

httpd = HTTPServer(("localhost", 8080), SimpleHandler)
print("Servidor rodando em http://localhost:8080")
httpd.serve_forever()