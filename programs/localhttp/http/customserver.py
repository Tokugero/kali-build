# TODO: Python script to start a generic server and parse out the following uris:
# /api?m=<input> (should be output as a string)
# /api?mb64=<input> (should parse out the base64 and output as a string)
# /api?c=<input> (should parse out the cookie and output as a string)
# /api?cb64 (should parse out the base64 and output as a string)
# /payload /target with index

import http.server
import socketserver
import os
import base64
import urllib.parse
import re
PORT = 4444

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/api?m='):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.log_message("m: %s", urllib.parse.unquote(self.path[7:]))
        elif self.path.startswith('/api?mb64='):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.log_message("m decoded: %s", base64.b64decode(urllib.parse.unquote(self.path[10:])))
        elif self.path.startswith('/api?c='):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.log_message("c: %s", urllib.parse.unquote(self.path[7:]))
        elif self.path.startswith('/api?cb64='):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.log_message("c decoded: %s", base64.b64decode(urllib.parse.unquote(self.path[10:])))
        # elif /api?file=.*p= then append contents of p to file name
        elif self.path.startswith('/api?file='):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            # Regex capture file=(.*)p=(.*)
            params = re.search(r'file=(.*)&p=(.*)', self.path)
            filename = params.group(1)
            if "/" in filename:
                self.log_message("Hackers detected!")
            else:
                payload = params.group(2)
                with open(filename, 'a') as f:
                    f.write(payload)
        elif self.path.startswith('/api?fileb64='):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            # Regex capture file=(.*)p=(.*)
            params = re.search(r'fileb64=(.*)&p=(.*)', self.path)
            filename = params.group(1)
            if "/" in filename:
                self.log_message("Hackers detected!")
            else:
                payload = base64.b64decode(params.group(2))
                with open(filename, 'a') as f:
                    f.write(payload.decode())
        elif self.path.startswith('/help'):
            # Print the options from above
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(b"Options: /api?m= /api?mb64= /api?c= /api?cb64= /api?file=.*&p=<payload> /api?file64=.*&p=<payload>")
        else:
            super().do_GET()

Handler = CustomHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    httpd.serve_forever()

# Run the server with the following command:
# python customserver.py
# Navigate to http://localhost:8000/api?m=hello to see the output