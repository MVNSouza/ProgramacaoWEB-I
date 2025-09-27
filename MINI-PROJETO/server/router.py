from .constants import allowed_methods


class Router:
    def __init__(self):
        self.routes = {}

    def add_route(self, endpoint, verbs):
        def wrapper(handler_fn):
            if endpoint in self.routes:
                raise Exception(f"A rota '{endpoint}' já está registrada!")

            self.routes[endpoint] = {}

            for verb in verbs:
                if verb not in allowed_methods:
                    raise Exception(f"Método HTTP inválido: '{verb}'")
                self.routes[endpoint][verb] = handler_fn

            return handler_fn

        return wrapper

    def handle_route(self, request, response):
        route_map = self.routes.get(request.path)

        if route_map is None:
            response.status_code = 404  # Rota não encontrada
            return

        action = route_map.get(request.method)

        if action is None or request.method not in allowed_methods:
            response.status_code = 405  # Método não permitido
            return

        try:
            action(request, response)
        except Exception:
            response.status_code = 500  # Erro interno
