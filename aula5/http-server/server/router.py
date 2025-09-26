from constants import allowed_methods

class Router:
    def __init__(self):
        self.routes = {}
    def add_route(self, path, methods):
        def register_route(handler):
                # validar se o caminho já foi registrado
                # Evita que duas funções tentem responder à mesma rota.
            if path in self.routes:
                raise Exception(f"A rota '{path}' já está registrada!")
            # validar os métodos e associar os handlers (manipuladores)
            self.routes[path] = {}
            for method in methods:
                if method not in allowed_methods:
                    raise Exception(f"Invalid HTTP method '{method}'")
                self.routes[path][method] = handler

            return handler
        return register_route

    def handle_route(self, request, response):
        route = self.routes.get(request.path)
        if route is None:
            response.status_code = 404
            return
        handler = route.get(request.method)
        if request.method not in allowed_methods or handler is None:
            response.status_code = 405
            return

        try:
            handler(request, response)
        except Exception:
            response.status_code = 500