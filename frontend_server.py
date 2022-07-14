"""
Simple Frontend HttpServer
"""

import os
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse
from urllib.request import Request, urlopen


HOST = '0.0.0.0'
PORT = os.environ.get('HTTP_PORT', 8081)
SIMPLE_API_URL = os.environ.get('SIMPLE_API_URL')

if not SIMPLE_API_URL:
    raise Exception("SIMPLE_API_URL must be set")


class SampleHandler(BaseHTTPRequestHandler):
    """
    request backend api http server
    """
    def do_GET(self):
        parsed_url = urlparse(self.path)
        url = f"{SIMPLE_API_URL}{parsed_url.path}?{parsed_url.query}"
        if url.find('favicon.ico') > 0:
            self.write_response(404, "".encode())
            return

        request = Request(url)
        with urlopen(request) as response:
            self.write_response(200, response.read())

    def write_response(self, status, body):
        self.send_response(status)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.send_header('Content-length', len(body))
        self.end_headers()
        self.wfile.write(body)


if __name__ == '__main__':
    httpd = HTTPServer((HOST, PORT), SampleHandler)
    print(f"start frontend server port={PORT}")
    httpd.serve_forever()
