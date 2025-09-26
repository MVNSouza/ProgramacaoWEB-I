# app.py
from flask import Flask, request, make_response, session, render_template_string, redirect, url_for, flash, get_flashed_messages
import datetime

# Inicializa a aplicação Flask
app = Flask(__name__)
# CHAVE SECRETA: ESSENCIAL para a segurança das sessões.
# Esta chave é usada para assinar criptograficamente os cookies de sessão.
# Em um ambiente de produção, use uma chave forte, gerada aleatoriamente
# (ex: os.urandom(24)) e carregada de uma variável de ambiente.
# NUNCA use uma chave fácil de adivinhar ou hardcoded em produção!
app.secret_key = 'uma_chave_secreta_muito_forte_e_aleatoria_para_o_projeto_1234567890'

# Rota principal para uma mensagem de boas-vindas e links de navegação
@app.route('/')
def index():
    messages = get_flashed_messages(with_categories=True)
    message_html = ""
    if messages:
        message_html = "<ul style='list-style: none; padding: 0;'>"
        for category, msg in messages:
            color = "#155724" if category == "success" else "#721c24"
            bg = "#d4edda" if category == "success" else "#f8d7da"
            border = "#c3e6cb" if category == "success" else "#f5c6cb"
            message_html += f"<li style='background-color: {bg}; color: {color}; border: 1px solid {border}; padding: 8px; margin-bottom: 5px; border-radius: 4px;'>{msg}</li>"
        message_html += "</ul>"
    # Verifica se o 'user_id' está na sessão (indicando que o usuário está logado)
    if 'user_id' in session:
        # Se logado, mostra links para dashboard e logout
        return f"""
        <h1>Bem-vindo, {session['user_id']}!</h1>
        <p>Você está logado.</p>
        <ul>
            <li><a href="/dashboard">Ir para o Dashboard (Área Restrita)</a></li>
            <li><a href="/logout">Logout</a></li>
        </ul>
        <hr>
        <p><h3>Demonstrações de Cookies (continuam funcionando independentemente da sessão):</h3></p>
        <ul>
            <li><a href="/definir-cookie-sessao">Definir cookie de sessão</a></li>
            <li><a href="/definir-cookie-persistente">Definir cookie persistente (expira após 7 dias)</a></li>
            <li><a href="/ler-cookie">Ler o cookie armazenado</a></li>
            <li><a href="/remover-cookie">Remover cookie</a></li>
            <li><a href="/contador-visitas">Contador de Visitas (com cookie)</a></li>
        </ul>
        """
    else:
        # Se não logado, mostra link para login
        return """
        <h1>Bem-vindo à aplicação de demonstração de Sessões e Cookies!</h1>
        <p>Este sistema simula operações básicas de gerenciamento de estado.</p>
        <ul>
            <li><a href="/login">Fazer Login</a></li>
        </ul>
        <hr>
        <p><h3>Demonstrações de Cookies:</h3></p>
        <ul>
            <li><a href="/definir-cookie-sessao">Definir cookie de sessão</a></li>
            <li><a href="/definir-cookie-persistente">Definir cookie persistente (expira após 7 dias)</a></li>
            <li><a href="/ler-cookie">Ler o cookie armazenado</a></li>
            <li><a href="/remover-cookie">Remover cookie</a></li>
            <li><a href="/contador-visitas">Contador de Visitas (com cookie)</a></li>
        </ul>
        """


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Se o usuário já está logado, redireciona para o dashboard imediatamente
    if 'user_id' in session:
        
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        # Processa os dados do formulário quando a requisição é POST
        username = request.form['username']
        password = request.form['password']

        # Simulação de autenticação (em um app real, você verificaria um banco de dados ou serviço de autenticação)
        if username == 'aluno' and password == '123': # Credenciais de exemplo
            # Login bem-sucedido: armazena o ID do usuário na sessão
            # 'session' é um objeto global do Flask que se comporta como um dicionário.
            # O Flask lida internamente com a criação do cookie de sessão assinado no navegador.
            session['user_id'] = username
            
            # Opcional: Para tornar a sessão persistente (durar mais que o fechamento do navegador),
            # descomente as linhas abaixo e defina um tempo de vida.
            session.permanent = True
            app.permanent_session_lifetime = datetime.timedelta(minutes=30) # Exemplo: sessão dura 30 minutos

            # Redireciona para a página do dashboard após o login
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('dashboard'))
        else:
            # Login falhou: exibe mensagem de erro e o formulário novamente
            flash('Credenciais inválidas.', 'error')
            return render_template_string("""
                <h1>Login</h1>
                <p style="color: red;">Credenciais inválidas. Tente novamente.</p>
                <form method="POST" action="/login">
                    <label for="username">Usuário:</label>
                    <input type="text" id="username" name="username" value="aluno"><br><br>
                    <label for="password">Senha:</label>
                    <input type="password" id="password" name="password" value="123"><br><br>
                    <button type="submit">Entrar</button>
                </form>
                <p><a href="/">Voltar à Página Inicial</a></p>
            """)
    else:
        # Exibe o formulário de login para requisições GET
        return render_template_string("""
            <h1>Login</h1>
            <form method="POST" action="/login">
                <label for="username">Usuário:</label>
                <input type="text" id="username" name="username" value="aluno"><br><br>
                <label for="password">Senha:</label>
                <input type="password" id="password" name="password" value="123"><br><br>
                <button type="submit">Entrar</button>
            </form>
            <p><a href="/">Voltar à Página Inicial</a></p>
        """)


@app.route('/dashboard')
def dashboard():

    if 'user_id' in session:
        messages = get_flashed_messages(with_categories=True)
        message_html = ""
        if messages:
            message_html = "<ul style='list-style: none; padding: 0;'>"
            for category, msg in messages:
                color = "#155724" if category == "success" else "#721c24"
                bg = "#d4edda" if category == "success" else "#f8d7da"
                border = "#c3e6cb" if category == "success" else "#f5c6cb"
                message_html += f"<li style='background-color: {bg}; color: {color}; border: 1px solid {border}; padding: 8px; margin-bottom: 5px; border-radius: 4px;'>{msg}</li>"
            message_html += "</ul>"

        return f"""
        {message_html}
        <h1>Bem-vindo ao Dashboard, {session['user_id']}!</h1>
        <p>Esta é uma área protegida por sessão.</p>
        <p>Aqui você poderia ver informações personalizadas ou acessar funcionalidades restritas.</p>
        <p><a href="/">Voltar à Página Inicial</a></p>
        <p><a href="/logout">Logout</a></p>
        """
    else:
        flash("Você precisa estar logado para acessar o dashboard.", "error")
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    # session.clear() remove todos os dados da sessão atual.
    # Isso efetivamente "desloga" o usuário, pois 'user_id' não estará mais na sessão.
    session.clear()
    # Redireciona para a página inicial após o logout
    return redirect(url_for('index'))

# Define um cookie de sessão (válido até o navegador ser fechado)
@app.route('/definir-cookie-sessao')
def definir_cookie_sessao():
   # make_response é usado para criar um objeto de resposta que podemos modificar
   resposta = make_response("Cookie de sessão 'usuario_logado' definido com sucesso.")
   # set_cookie é o método que adiciona o cabeçalho 'Set-Cookie' na resposta HTTP.
   # Por padrão, se 'max_age' ou 'expires' não forem definidos, será um cookie de sessão.
   resposta.set_cookie('usuario_logado', 'admin', httponly = True, secure = True)
   return resposta

# Define um cookie persistente com validade de 7 dias
@app.route('/definir-cookie-persistente')
def definir_cookie_persistente():
   resposta = make_response("Cookie persistente 'token_autenticacao' definido. Ele expira em 7 dias.")
   # Usamos o parâmetro 'max_age' para definir a duração do cookie em segundos.
   # 60 segundos * 60 minutos * 24 horas * 7 dias = 604800 segundos.
   resposta.set_cookie('token_autenticacao', 'abc123DEF456', httponly = True, secure = True, max_age=60*60*24*7)
  
   return resposta

# Lê os cookies recebidos na requisição
@app.route('/ler-cookie')
def ler_cookie():
   # request.cookies é um objeto tipo dicionário que contém todos os cookies
   # que o navegador enviou com a requisição atual.
   # Usamos .get() para evitar erros se o cookie não existir.
   usuario = request.cookies.get('usuario_logado', 'Nenhum cookie de sessão encontrado.')
   token = request.cookies.get('token_autenticacao', 'Nenhum cookie persistente encontrado.')
   return f"""
   <h1>Cookies Atuais</h1>
   <p>Valor do cookie de sessão <strong>'usuario_logado'</strong>: <strong>{usuario}</strong></p>
   <p>Valor do cookie persistente <strong>'token_autenticacao'</strong>: <strong>{token}</strong></p>
   <p><a href="/">Voltar à Página Inicial</a></p>
   """

# Remove os cookies do navegador
@app.route('/remover-cookie')
def remover_cookie():
   resposta = make_response("Cookies 'usuario_logado' e 'token_autenticacao' removidos com sucesso.")
   # Para remover um cookie, definimos seu valor como vazio e sua data de expiração no passado (expires=0).
   # O navegador, ao receber este Set-Cookie, entende que deve apagar o cookie.
   resposta.set_cookie('usuario_logado', '', expires=0)
   resposta.set_cookie('token_autenticacao', '', expires=0)
   return resposta


@app.route("/contador-visitas")
def contador_visitas():
   # Tenta ler o cookie 'visitas_count'
   visitas = request.cookies.get('visitas_count')


   if visitas:
       try:
           visitas = int(visitas) + 1
       except ValueError:
           visitas = 1  # Valor inválido no cookie, reinicia o contador
   else:
       visitas = 1  # Cookie não existe, inicializa


   # Cria a resposta HTML
   mensagem = f"<html><body><h1>Você visitou esta página {visitas} vezes.</h1></body></html>"
   resposta = make_response(mensagem)


   # Define cookie persistente por 1 ano (365 dias)
   resposta.set_cookie('visitas_count', str(visitas), max_age=60 * 60 * 24 * 365)


   return resposta


@app.route('/adicionar-ao-carrinho/<item_nome>')
def adicionar_ao_carrinho(item_nome):
    # 1) Garante que existe a chave 'carrinho' (lista) na sessão
    carrinho = session.get('carrinho', [])
    carrinho.append(item_nome)
    session['carrinho'] = carrinho

    # 2) Gera mensagem manualmente (sem usar flash, opcional aqui)
    return f"""
    <h1>Item Adicionado</h1>
    <p>O item <strong>{item_nome}</strong> foi adicionado ao seu carrinho.</p>
    <p>
        <a href="/ver-carrinho">Ver carrinho</a> |
        <a href="/">Voltar à Página Inicial</a>
    </p>
    """


@app.route('/ver-carrinho')
def ver_carrinho():
    """
    Exibe os itens atualmente no carrinho.
    """
    # Bloco de mensagens flash reutilizado
    messages = get_flashed_messages(with_categories=True)
    message_html = ""
    if messages:
        message_html = "<ul style='list-style: none; padding: 0;'>"
        for category, msg in messages:
            color = "#155724" if category == "success" else "#721c24"
            bg = "#d4edda" if category == "success" else "#f8d7da"
            border = "#c3e6cb" if category == "success" else "#f5c6cb"
            message_html += f"<li style='background-color: {bg}; color: {color}; border: 1px solid {border}; padding: 8px; margin-bottom: 5px; border-radius: 4px;'>{msg}</li>"
        message_html += "</ul>"

    # Recupera carrinho (lista) – se não existir, mostra vazio
    carrinho = session.get('carrinho', [])

    # Monta lista de itens ou aviso de carrinho vazio
    if carrinho:
        itens_html = "<ul>" + "".join(f"<li>{item}</li>" for item in carrinho) + "</ul>"
    else:
        itens_html = "<p><em>Seu carrinho está vazio.</em></p>"

    return f"""
    {message_html}
    <h1>Meu Carrinho</h1>
    {itens_html}
    <p>
        <a href="/">Voltar à Página Inicial</a> |
        <a href="/limpar-carrinho">Limpar Carrinho</a>
    </p>
    """


@app.route('/limpar-carrinho')
def limpar_carrinho():
    """
    Esvazia o carrinho na sessão.
    """
    session['carrinho'] = []  # ou session.pop('carrinho', None)
    flash("Carrinho limpo com sucesso.", "success")
    return redirect(url_for('ver_carrinho'))

# Fim das Rotas


# Bloco para rodar a aplicação quando o script é executado diretamente
if __name__ == '__main__':
   app.run(debug=True) # debug=True ativa o modo de depuração (reinicia ao salvar e mostra erros)

