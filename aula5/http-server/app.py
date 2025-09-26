from server import Server
from urllib.parse import parse_qs

app = Server()

@app.route("/usuarios")
def index(request, response):
    response.headers["Content-Type"] = "text/html; charset=utf-8"
    response.body = """<!DOCTYPE html>
<html>
<head>
  <title>Saudação</title>
</head>
<body>
  <form action="/saudar" method="POST">
    <label for="name">
      Digite seu nome:
      <input type="text" name="name">
    </label>
    <input type="submit">
  </form>
</body>
</html>
"""

@app.route("/usuarios", methods=["POST"])
def saudar(request, response):
    data = parse_qs(request.body)
    name = data.get("name", [""])[0]
    response.headers["Content-Type"] = "text/html; charset=utf-8"
    response.body = f"""<!DOCTYPE html>
<html>
<head>
  <title>Olá!</title>
</head>
<body>
  <p>Olá, {name}!</p>
  <a href="/">Tente novamente</a>
</body>
</html>
"""

if __name__ == "__main__":
    app.start(port=3000)
