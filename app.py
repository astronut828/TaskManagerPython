from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
from routes.delete import handle_delete
from routes.update import handle_update
from routes.create import handle_create
from routes.index import handle_fetch
from models import create_tasks_table

class CRUDHandler (BaseHTTPRequestHandler):
    
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/":
            handle_fetch(self)
            
        elif path == "/create":
            with open("templates/create.html", "r") as f:
                html = f.read()
            self._send_html(html)

        elif path == "/delete":
            handle_delete(self)

        elif path == "/update":
            html = handle_update(self)
            self._send_html(html)

        else:
            self.send_error(404, "Page not found")
            
    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/create":
            handle_create(self)

        elif path == "/update":
            handle_update(self)

        else:
            self.send_error(404, "Page not found")

    def _send_html(self, html):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(html.encode())


if __name__ == "__main__":
    create_tasks_table()
    server_address = ('',8000)
    httpd = HTTPServer(server_address,CRUDHandler)
    print("Server is running on http://localhost:8080")
    httpd.serve_forever()