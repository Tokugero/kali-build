import http.server
import socketserver
import os
import base64
import urllib.parse
import re

PORT = int(os.environ.get('PORT', 4444))

ENDPOINTS = {
    "/api?m=<input>": "Echoes the input as a string.",
    "/api?mb64=<base64input>": "Decodes base64 input and echoes the result as a string.",
    "/api?c=<input>": "Echoes the input as a string (cookie format).",
    "/api?cb64=<base64input>": "Decodes base64 input (cookie format) and echoes the result as a string.",
    "/api?file=<filename>&p=<payload>": "Appends the payload to the specified file (filename must not contain '/').",
    "/api?fileb64=<filename>&p=<base64payload>": "Decodes base64 payload and appends to the specified file (filename must not contain '/').",
    "/help": "Lists all available endpoints and their descriptions."
}

def parse_post_data(handler):
    content_length = int(handler.headers.get('Content-Length', 0))
    body = handler.rfile.read(content_length).decode()
    return urllib.parse.parse_qs(body)

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def respond(self, msg):
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        if isinstance(msg, str):
            self.wfile.write(msg.encode())
        else:
            self.wfile.write(msg)

    def show_endpoints(self):
        msg = "Available endpoints:\n\n"
        for ep, desc in ENDPOINTS.items():
            msg += f"{ep}\n    {desc}\n\n"
        self.respond(msg)

    def handle_api(self, method='GET', params=None):
        # Parse GET or POST parameters
        if method == 'GET':
            query = urllib.parse.urlparse(self.path).query
            params = urllib.parse.parse_qs(query)
        elif params is None:
            params = {}

        # /api?m=<input>
        if 'm' in params:
            self.respond(urllib.parse.unquote(params['m'][0]))
        # /api?mb64=<input>
        elif 'mb64' in params:
            try:
                decoded = base64.b64decode(urllib.parse.unquote(params['mb64'][0])).decode()
                self.respond(decoded)
            except Exception as e:
                self.respond(f"Invalid base64: {e}")
        # /api?c=<input>
        elif 'c' in params:
            self.respond(urllib.parse.unquote(params['c'][0]))
        # /api?cb64=<input>
        elif 'cb64' in params:
            try:
                decoded = base64.b64decode(urllib.parse.unquote(params['cb64'][0])).decode()
                self.respond(decoded)
            except Exception as e:
                self.respond(f"Invalid base64: {e}")
        # /api?file=<filename>&p=<payload>
        elif 'file' in params and 'p' in params:
            filename = params['file'][0]
            if "/" in filename:
                self.respond("Hackers detected!")
            else:
                payload = params['p'][0]
                with open(filename, 'a') as f:
                    f.write(payload)
                self.respond(f"Payload appended to {filename}")
        # /api?fileb64=<filename>&p=<payload>
        elif 'fileb64' in params and 'p' in params:
            filename = params['fileb64'][0]
            if "/" in filename:
                self.respond("Hackers detected!")
            else:
                try:
                    payload = base64.b64decode(params['p'][0]).decode()
                    with open(filename, 'a') as f:
                        f.write(payload)
                    self.respond(f"Decoded payload appended to {filename}")
                except Exception as e:
                    self.respond(f"Invalid base64: {e}")
        else:
            self.respond("Invalid API call. See /help for options.")

    def do_GET(self):
        if self.path.startswith('/help'):
            self.show_endpoints()
        elif self.path.startswith('/api'):
            self.handle_api(method='GET')
        else:
            super().do_GET()

    def do_POST(self):
        if self.path.startswith('/api'):
            params = parse_post_data(self)
            self.handle_api(method='POST', params=params)
        elif self.path.startswith('/help'):
            self.show_endpoints()
        else:
            super().do_POST()


Handler = CustomHandler

def print_endpoints():
    print("Available endpoints:\n")
    for ep, desc in ENDPOINTS.items():
        print(f"{ep}\n    {desc}\n")
    print(f"\nServer is running on port {PORT}\n")

if __name__ == "__main__":
    print_endpoints()
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        httpd.serve_forever()
