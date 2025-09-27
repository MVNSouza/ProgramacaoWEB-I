from datetime import datetime
from urllib import parse
from .constants import status_codes


class Request:
    def __init__(self, raw_bytes, client_addr):
        # Converte os bytes da requisição em texto
        raw_text = raw_bytes.decode("utf-8")

        # Divide entre cabeçalho e corpo
        head_section, body_section = raw_text.split("\r\n\r\n", 1)
        first_line, *other_lines = head_section.split("\r\n")

        # Exemplo: GET /rota HTTP/1.1
        verb, resource, version = first_line.split(" ")
        parsed_url = parse.urlparse(resource)

        self.datetime = datetime.now()
        self.ip = client_addr[0]
        self.method = verb
        self.uri = resource
        self.path = parsed_url.path
        self.queries = parse.parse_qs(parsed_url.query)
        self.http_version = version
        self.headers = self.parse_headers(other_lines)
        self.body = body_section

    def parse_headers(self, lines):
        parsed_headers = {}
        for item in lines:
            if ":" in item:
                header_key, header_val = item.split(":", 1)
                parsed_headers[header_key.lower()] = header_val.strip()
        return parsed_headers


class Response:
    def __init__(self, headers=None, body="", status_code=200, status_message=None):
        self.headers = headers or {"Content-Type": "text/html; charset=utf-8"}
        self.body = body
        self.status_code = status_code

        self._custom_status = status_message is not None
        self._status_text = status_message or "???"

    @property
    def status_message(self):
        if not self._custom_status:
            return status_codes.get(self.status_code, "???")
        return self._status_text

    @status_message.setter
    def status_message(self, new_text):
        self._status_text = new_text
        self._custom_status = True

    def serialize(self):
        line = f"HTTP/1.1 {self.status_code} {self.status_message}"
        hdrs = "\r\n".join([f"{k}: {v}" for k, v in self.headers.items()])
        block = "\r\n".join([line, hdrs])
        full_response = "\r\n\r\n".join([block, self.body])
        return full_response.encode("utf-8")
