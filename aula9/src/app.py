
import logging, json, os
from flask import Flask, request, session, render_template, redirect, url_for
from flask_jwt_extended import JWTManager, create_access_token, decode_token
from flask_httpauth import HTTPBasicAuth
from helper import load_users, add_user, delete_user, find_user, save_users
from config import SECRET_KEY, JWT_SECRET_KEY, LOG_LEVEL, USERS_FILE
from logs import log_login_attempt, log_login_result, log_jwt_issue, log_protected_access

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))   # Caminho absoluto da pasta principal do projeto
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")                          # Caminho da pasta de templates HTML
STATIC_DIR = os.path.join(BASE_DIR, "static")                               # Caminho da pasta de arquivos estáticos      

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)
app.secret_key = SECRET_KEY                     # Define a chave secreta da sessão do Flask
app.config["JWT_SECRET_KEY"] = JWT_SECRET_KEY   # Define a chave secreta para tokens JWT

# Configura o logger global com nível e formato definido
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL, logging.DEBUG),
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

# --- Autenticação ---
jwt = JWTManager(app)
basic_auth = HTTPBasicAuth()

# --- Verifica usuário e senha para autenticação básica ---
@basic_auth.verify_password
def verify_basic(username, password):
    user = find_user(username)
    if user and user["password"] == password:
        return user
    return None

# --- Retorna a role/permissão do usuário ---
@basic_auth.get_user_roles
def get_user_roles(user):
    return user["role"]

# --- Login JWT ---
@app.route("/login/jwt", methods=["GET", "POST"])
def login_jwt_page():
    if request.method == "GET":
        return render_template("login_jwt.html")
    
    username = request.form.get("username")
    password = request.form.get("password")
    log_login_attempt(username, password)
    
    user = find_user(username)
    if user and user["password"] == password:
        payload = {"username": username, "role": user["role"]}
        token = create_access_token(identity=json.dumps(payload))
        session["jwt_token"] = token
        session["user"] = payload
        log_login_result(username, True)
        log_jwt_issue(username, payload)
        return redirect(url_for("protected"))
    
    log_login_result(username, False, "Credenciais inválidas")
    return render_template("login_jwt.html", error="Credenciais inválidas")

# --- Login Sessão ---
@app.route("/login/session", methods=["GET", "POST"])
def login_session_page():
    if request.method == "GET":
        return render_template("login_session.html")
    
    username = request.form.get("username")
    password = request.form.get("password")
    log_login_attempt(username, password)
    
    user = find_user(username)
    if user and user["password"] == password:
        session["user"] = {"username": username, "role": user["role"]}
        log_login_result(username, True)
        return redirect(url_for("protected"))
    
    log_login_result(username, False, "Credenciais inválidas")
    return render_template("login_session.html", error="Credenciais inválidas")

# --- Login Basic Auth ---
@app.route("/login/basic")
@basic_auth.login_required
def login_basic():
    user = basic_auth.current_user()
    session["user"] = {"username": user["username"], "role": user["role"]}
    log_login_result(user["username"], True)
    return redirect(url_for("protected"))

# --- Autenticação unificada ---
def get_authenticated_user():
    if "user" in session:
        return session["user"]
    if "jwt_token" in session:
        try:
            decoded = decode_token(session["jwt_token"])
            return json.loads(decoded["sub"])
        except:
            return None
    if basic_auth.current_user():
        u = basic_auth.current_user()
        return {"username": u["username"], "role": u["role"]}
    return None

# --- Protected ---
@app.route("/protected")
def protected():
    user = get_authenticated_user()
    if not user:
        return redirect(url_for("login"))
    log_protected_access(user)
    token = session.get("jwt_token")
    return render_template("protected.html", user=user, token=token)

# --- CRUD Admin ---
@app.route("/admin/users", methods=["GET", "POST"])
@basic_auth.login_required(optional=True)
def admin_users_route():
    user = get_authenticated_user()
    if not user or user["role"] != "admin":
        return "Acesso negado", 403
    
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        role = request.form.get("role", "user")
        add_user(username, password, role)
    
    users_list = load_users()
    return render_template("admin_users.html", users=users_list, current_user=user)

@app.route("/admin/users/delete/<username>", methods=["POST"])
@basic_auth.login_required(optional=True)
def delete_user_route(username):
    user = get_authenticated_user()
    if not user or user["role"] != "admin":
        return "Acesso negado", 403
    delete_user(username)
    return redirect(url_for("admin_users_route"))

# --- Logout ---
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

# --- Página de login com escolha de sessão ---
@app.route("/login")
def login():
    return render_template("login.html")

# --- Home ---
@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)
