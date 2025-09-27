# Métodos HTTP permitidos, conforme a especificação do protocolo
allowed_methods = {
    "GET",       # Recupera dados do servidor (ex: carregar uma página)
    "HEAD",      # Igual ao GET, mas sem o corpo da resposta
    "POST",      # Envia dados para o servidor (ex: formulários)
    "PUT",       # Substitui o recurso no servidor
    "DELETE",    # Remove um recurso
    "CONNECT",   # Estabelece um túnel para comunicação segura (ex: HTTPS)
    "OPTIONS",   # Retorna os métodos suportados pelo servidor
    "TRACE",     # Ecoa a requisição recebida para diagnóstico
    "PATCH"      # Atualiza parcialmente um recurso
}

# Dicionário com os códigos de status HTTP e suas descrições
status_codes = {
    100: "Continuar",
    101: "Trocando Protocolos",
    200: "OK",
    201: "Criado",
    202: "Aceito",
    203: "Informação Não-Autorizada",
    204: "Sem Conteúdo",
    205: "Redefinir Conteúdo",
    206: "Conteúdo Parcial",
    300: "Múltiplas Escolhas",
    301: "Movido Permanentemente",
    302: "Encontrado",
    303: "Ver Outro",
    304: "Não Modificado",
    305: "Usar Proxy",
    307: "Redirecionamento Temporário",
    400: "Requisição Inválida",
    401: "Não Autorizado",
    402: "Pagamento Necessário",
    403: "Proibido",
    404: "Não Encontrado",
    405: "Método Não Permitido",
    406: "Não Aceitável",
    407: "Autenticação de Proxy Necessária",
    408: "Tempo de Requisição Esgotado",
    409: "Conflito",
    410: "Removido",
    411: "Comprimento Necessário",
    412: "Pré-condição Falhou",
    413: "Carga Muito Grande",
    414: "URI Muito Longo",
    415: "Tipo de Mídia Não Suportado",
    416: "Faixa Não Satisfatória",
    417: "Expectativa Falhou",
    418: "Sou um bule de chá",
    426: "Atualização Necessária",
    500: "Erro Interno no Servidor",
    501: "Não Implementado",
    502: "Gateway Inválido",
    503: "Serviço Indisponível",
    504: "Tempo do Gateway Esgotado",
    505: "Versão HTTP Não Suportada"
}