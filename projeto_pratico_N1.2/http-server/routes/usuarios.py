import os
from urllib.parse import unquote

USUARIOS_FILE = os.path.join(os.path.dirname(__file__), '..', 'usuarios.txt')

def carregar_usuarios():
    """Carrega todos os usuários do arquivo texto"""
    if not os.path.exists(USUARIOS_FILE):
        return []
    
    usuarios = []
    with open(USUARIOS_FILE, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            if line.strip():
                id, nome, email, telefone = line.strip().split('|')
                usuarios.append({
                    'id': int(id),
                    'nome': unquote(nome),
                    'email': unquote(email),
                    'telefone': unquote(telefone)
                })
    return usuarios

def salvar_usuarios(usuarios):
    """Salva a lista de usuários no arquivo texto"""
    with open(USUARIOS_FILE, 'w', encoding='utf-8') as f:
        for usuario in usuarios:
            linha = "|".join([
                str(usuario['id']),
                usuario['nome'],
                usuario['email'],
                usuario['telefone']
            ]) + "\n"
            f.write(linha)

def obter_proximo_id(usuarios):
    """Obtém o próximo ID disponível"""
    return max([u['id'] for u in usuarios], default=0) + 1

def listar_usuarios(request, response):
    """Lista todos os usuários em formato HTML"""
    usuarios = carregar_usuarios()
    
    html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Lista de Usuarios</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        table { width: 100%; border-collapse: collapse; margin-top: 20px; }
        th, td { padding: 10px; border: 1px solid #ddd; text-align: left; }
        th { background-color: #f2f2f2; }
        tr:nth-child(even) { background-color: #f9f9f9; }
        .actions { white-space: nowrap; }
        .actions a, .actions button { margin-right: 5px; }
    </style>
</head>
<body>
    <h1>Lista de Usuários</h1>
    <a href="/usuarios/novo" style="padding: 8px 12px; background: #4CAF50; color: white; text-decoration: none; border-radius: 4px;">Novo Usuario</a>
    <table>
        <thead>
            <tr>
                <th>ID</th>
                <th>Nome</th>
                <th>Email</th>
                <th>Telefone</th>
                <th>Ações</th>
            </tr>
        </thead>
        <tbody>"""
    
    for usuario in usuarios:
        html += f"""
            <tr>
                <td>{usuario['id']}</td>
                <td>{usuario['nome']}</td>
                <td>{usuario['email']}</td>
                <td>{usuario['telefone']}</td>
                <td class="actions">
                    <a href="/usuarios/{usuario['id']}" style="color: #2196F3;">Ver</a>
                    <a href="/usuarios/{usuario['id']}/editar" style="color: #FFC107;">Editar</a>
                    <form action="/usuarios/{usuario['id']}/excluir" method="POST" style="display: inline;">
                        <button type="submit" style="background: #F44336; color: white; border: none; padding: 5px 10px; border-radius: 3px; cursor: pointer;">Excluir</button>
                    </form>
                </td>
            </tr>"""
    
    html += """
        </tbody>
    </table>
</body>
</html>"""
    
    response.body = html

def novo_usuario(request, response):
    """Exibe formulário para criar novo usuário"""

    response.body = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Novo Usuario</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        form { max-width: 500px; }
        .form-group { margin-bottom: 15px; }
        label { display: block; margin-bottom: 5px; }
        input { width: 100%; padding: 8px; box-sizing: border-box; }
        button { padding: 8px 15px; background: #4CAF50; color: white; border: none; border-radius: 4px; }
    </style>
</head>
<body>
    <h1>Novo Usuario</h1>
    <form method="POST" action="/usuarios">
        <div class="form-group">
            <label for="nome">Nome:</label>
            <input type="text" id="nome" name="nome" required>
        </div>
        <div class="form-group">
            <label for="email">Email:</label>
            <input type="email" id="email" name="email" required>
        </div>
        <div class="form-group">
            <label for="telefone">Telefone:</label>
            <input type="tel" id="telefone" name="telefone" required>
        </div>
        <button type="submit">Salvar</button>
        <a href="/usuarios" style="margin-left: 10px;">Cancelar</a>
    </form>
</body>
</html>"""

def criar_usuario(request, response):
    """Processa a criação de um novo usuário"""
    usuarios = carregar_usuarios()
    novo_id = obter_proximo_id(usuarios)
    
    novo_usuario = {
        'id': novo_id,
        'nome': request.body['nome'][0],
        'email': request.body['email'][0],
        'telefone': request.body['telefone'][0]
    }
    
    usuarios.append(novo_usuario)
    salvar_usuarios(usuarios)
    
    response.status_code = 302
    response.headers['Location'] = '/usuarios'

def detalhar_usuario(request, response, id):
    """Exibe os detalhes de um usuário específico"""
    usuarios = carregar_usuarios()
    usuario = next((u for u in usuarios if u['id'] == int(id)), None)
    
    if not usuario:
        response.status_code = 404
        response.body = "<h1>Usuario nao encontrado</h1>"
        return

    response.body = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Detalhes do Usuario</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .user-details {{ background: #f9f9f9; padding: 20px; border-radius: 5px; }}
        .actions {{ margin-top: 20px; }}
        .actions a, .actions button {{ margin-right: 10px; }}
    </style>
</head>
<body>
    <h1>Detalhes do Usuario</h1>
    <div class="user-details">
        <p><strong>ID:</strong> {usuario['id']}</p>
        <p><strong>Nome:</strong> {usuario['nome']}</p>
        <p><strong>Email:</strong> {usuario['email']}</p>
        <p><strong>Telefone:</strong> {usuario['telefone']}</p>
    </div>
    <div class="actions">
        <a href="/usuarios/{usuario['id']}/editar" style="padding: 8px 12px; background: #FFC107; color: black; text-decoration: none; border-radius: 4px;">Editar</a>
        <form action="/usuarios/{usuario['id']}/excluir" method="POST" style="display: inline;">
            <button type="submit" style="padding: 8px 12px; background: #F44336; color: white; border: none; border-radius: 4px; cursor: pointer;">Excluir</button>
        </form>
        <a href="/usuarios" style="padding: 8px 12px; background: #9E9E9E; color: white; text-decoration: none; border-radius: 4px;">Voltar</a>
    </div>
</body>
</html>"""

def editar_usuario(request, response, id):
    """Exibe formulário para editar um usuário"""
    usuarios = carregar_usuarios()
    usuario = next((u for u in usuarios if u['id'] == int(id)), None)
    
    if not usuario:
        response.status_code = 404
        response.body = "<h1>Usuario nao encontrado</h1>"
        return
    
    response.body = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Editar Usuario</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        form {{ max-width: 500px; }}
        .form-group {{ margin-bottom: 15px; }}
        label {{ display: block; margin-bottom: 5px; }}
        input {{ width: 100%; padding: 8px; box-sizing: border-box; }}
        button {{ padding: 8px 15px; background: #4CAF50; color: white; border: none; border-radius: 4px; }}
    </style>
</head>
<body>
    <h1>Editar Usuario</h1>
    <form method="POST" action="/usuarios/{usuario['id']}/atualizar">
        <div class="form-group">
            <label for="nome">Nome:</label>
            <input type="text" id="nome" name="nome" value="{usuario['nome']}" required>
        </div>
        <div class="form-group">
            <label for="email">Email:</label>
            <input type="email" id="email" name="email" value="{usuario['email']}" required>
        </div>
        <div class="form-group">
            <label for="telefone">Telefone:</label>
            <input type="tel" id="telefone" name="telefone" value="{usuario['telefone']}" required>
        </div>
        <button type="submit">Atualizar</button>
        <a href="/usuarios/{usuario['id']}" style="margin-left: 10px;">Cancelar</a>
    </form>
</body>
</html>"""

def atualizar_usuario(request, response, id):
    """Processa a atualização de um usuário"""
    usuarios = carregar_usuarios()
    usuario = next((u for u in usuarios if u['id'] == int(id)), None)
    
    if not usuario:
        response.status_code = 404
        response.body = "<h1>Usuario nao encontrado</h1>"
        return
    
    usuario['nome'] = request.body['nome'][0]
    usuario['email'] = request.body['email'][0]
    usuario['telefone'] = request.body['telefone'][0]
    
    salvar_usuarios(usuarios)
    
    response.status_code = 302
    response.headers['Location'] = f'/usuarios/{id}'


def excluir_usuario(request, response, id):
    """Remove um usuário do sistema e realoca os IDs"""
    usuarios = carregar_usuarios()
    usuarios = [u for u in usuarios if u['id'] != int(id)]
    """Atualiza os IDS dos usuarios ja cadastros apos a exclusão"""
    for id_user, usuario in enumerate(usuarios, start=1):
        usuario['id'] = id_user
    salvar_usuarios(usuarios)
    
    response.status_code = 302
    response.headers['Location'] = '/usuarios'
