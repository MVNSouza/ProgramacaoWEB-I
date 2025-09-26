import logging
from flask import request

logger = logging.getLogger(__name__)
# --- Funções de log ---
# Registra a tentativa de login com username, senha mascarada e IP do cliente
def log_login_attempt(username, password):
    masked_pw = "*" * len(password) if password else ""
    ip = request.remote_addr
    logger.debug(f"Tentativa de login: username={username}, senha={masked_pw}, IP={ip}")

# Registra o resultado do login com username, sucesso/falha e motivo
def log_login_result(username, success, reason=""):
    logger.debug(f"Login {'SUCESSO' if success else 'FALHA'} para {username}. {reason}")

# Registra a emissão de um token JWT com username e payload
def log_jwt_issue(username, payload):
    logger.debug(f"JWT emitido para {username}. Payload: {payload}")

# Registra o acesso a uma rota protegida com username e role do usuário
def log_protected_access(user):
    logger.debug(f"Acesso à rota protegida: usuário={user['username']}, role={user['role']}")