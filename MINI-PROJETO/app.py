import os
from server import Server
from urllib.parse import parse_qs
import mimetypes  # Para definir o tipo de conteúdo correto

app = Server()

# Rota principal
@app.route("/")
def index(request, response):
    file_path = os.path.join("static", "index.html")
    if not os.path.exists(file_path):
        response.status_code = 404
        response.body = "<h1>Arquivo não encontrado</h1>"
        return
    
    with open(file_path, "r", encoding="utf-8") as f:
        response.body = f.read()
        response.headers["Content-Type"] = "text/html"

# Rota para servir CSS, JS, imagens etc.
@app.route("/static/<path:file_path>")
def static_files(request, response, file_path):
    full_path = os.path.join("static", file_path)
    if not os.path.exists(full_path):
        response.status_code = 404
        response.body = "<h1>Arquivo não encontrado</h1>"
        return
    
    # Define o Content-Type automaticamente
    mime_type, _ = mimetypes.guess_type(full_path)
    response.headers["Content-Type"] = mime_type or "application/octet-stream"

    with open(full_path, "rb") as f:
        response.body = f.read()

# Rota de saudação
@app.route("/saudar", methods=["POST"])
def greet(request, response):
    data = parse_qs(request.body)
    user_name = data.get("name", [""])[0]

    response.body = f"""<!DOCTYPE html>
<html>
<head>
  <title>Olá!</title>
</head>
<body>
  <p>Olá, {user_name}!</p>
  <a href="/">Tente novamente</a>
</body>
</html>
"""
    response.headers["Content-Type"] = "text/html"

if __name__ == "__main__":
    app.start(host="0.0.0.0", port=3000)
