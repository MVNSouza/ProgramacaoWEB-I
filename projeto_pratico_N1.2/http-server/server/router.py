import re
from .plumbing import Request, Response

class Router:
    def __init__(self):
        self.routes = []

    def add_route(self, path, methods=None):
        if methods is None:
            methods = ['GET']
        
        def decorator(handler):
            self.routes.append({
                'pattern': re.compile(f'^{path}$'),
                'methods': [m.upper() for m in methods],
                'handler': handler
            })
            return handler
        return decorator

    def handle_route(self, request, response):
        for route in self.routes:
            match = route['pattern'].match(request.path)
            if match and request.method in route['methods']:
                route['handler'](request, response, **match.groupdict())
                return
        
        response.status_code = 404
        response.body = "<h1>404 Not Found</h1>"
        response.headers['Content-Type'] = 'text/html'