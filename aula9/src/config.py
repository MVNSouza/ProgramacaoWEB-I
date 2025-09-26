import os

# Chaves secretas
SECRET_KEY = os.environ.get("SECRET_KEY", "chave_secreta_session")
JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "chave_secreta_jwt")

# Configurações de debug/log
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO").upper()

# Arquivo de usuários
BASE_DIR = os.path.dirname(__file__)
USERS_FILE = os.path.join(BASE_DIR, "users.json")
