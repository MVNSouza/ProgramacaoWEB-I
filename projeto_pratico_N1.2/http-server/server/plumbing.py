from urllib.parse import parse_qs, urlparse
from .constants import status_codes

class Request:
    def __init__(self, request_data):
        self.raw_data = request_data.decode('utf-8')
        self.method, self.path, self.protocol = self._parse_request_line()
        self.headers = self._parse_headers()
        self.body = self._parse_body()
        self.query = self._parse_query()

    def _parse_request_line(self):
        lines = self.raw_data.split('\r\n')
        return lines[0].split() if lines else ('GET', '/', 'HTTP/1.1')

    def _parse_headers(self):
        lines = self.raw_data.split('\r\n')[1:]
        headers = {}
        for line in lines:
            if not line:
                break
            key, value = line.split(': ', 1)
            headers[key] = value
        return headers

    def _parse_body(self):
        parts = self.raw_data.split('\r\n\r\n')
        return parse_qs(parts[1]) if len(parts) > 1 else {}

    def _parse_query(self):
        return parse_qs(urlparse(self.path).query)

class Response:
    def __init__(self):
        self.status_code = 200
        self.headers = {'Content-Type': 'text/html'}
        self.body = ""
    
    def serialize(self):
        status_line = f"HTTP/1.1 {self.status_code} {status_codes.get(self.status_code, '')}\r\n"
        headers = '\r\n'.join(f"{k}: {v}" for k, v in self.headers.items())
        return f"{status_line}{headers}\r\n\r\n{self.body}".encode('utf-8')