import json
import os
from config import USERS_FILE

# Carrega a lista de usuários do arquivo JSON.
def load_users():
    if not os.path.exists(USERS_FILE):
        return []
    with open(USERS_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# alva a lista de usuários no arquivo JSON.
def save_users(users):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, indent=4, ensure_ascii=False)

# Retorna o usuário com o username dado, ou None.
def find_user(username):
    users = load_users()
    return next((u for u in users if u["username"] == username), None)

# Adiciona um novo usuário à lista e salva no arquivo.
def add_user(user):
    users = load_users()
    users.append(user)
    save_users(users)

# Deleta um usuário pelo username e salva a lista atualizada no arquivo.
def delete_user(username):
    users = load_users()
    users = [u for u in users if u["username"] != username]
    save_users(users)
