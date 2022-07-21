"""
Simple Frontend HttpServer
"""

import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
from urllib.request import Request, urlopen


HOST = '0.0.0.0'
PORT = int(os.environ.get('HTTP_PORT', '80'))

SIMPLE_API_HOST = os.environ.get('COPILOT_SERVICE_DISCOVERY_ENDPOINT')
if SIMPLE_API_HOST is None:
    SIMPLE_API_HOST = 'api'
else:
    SIMPLE_API_HOST = f'api.{SIMPLE_API_HOST}'

SIMPLE_API_PORT = os.environ.get('SIMPLE_API_PORT', 8082)
SIMPLE_API_URL = f'http://{SIMPLE_API_HOST}:{SIMPLE_API_PORT}'


class SampleHandler(BaseHTTPRequestHandler):
    """
    request backend api http server
    """
    def do_GET(self):
        parsed_url = urlparse(self.path)
        
        if '/' == parsed_url.path:
            self.write_response(200, "OK".encode())
            return

        if parsed_url.path.find("/api") == 0:
            api_path = parsed_url.path[4:]
            url = f"{SIMPLE_API_URL}{api_path}"
            if parsed_url.query is not None:
                url += f"?{parsed_url.query}"

            request = Request(url)
            with urlopen(request) as response:
                self.write_response(200, response.read())

        else:
            self.write_response(404, "".encode())
            return

    def write_response(self, status, body):
        self.send_response(status)
        self.send_header('Content-type', 'text/plain; charset=utf-8')
        self.send_header('Content-length', len(body))
        self.end_headers()
        self.wfile.write(body)


if __name__ == '__main__':
    httpd = HTTPServer((HOST, PORT), SampleHandler)
    print(f"start frontend server port={PORT}")
    httpd.serve_forever()
