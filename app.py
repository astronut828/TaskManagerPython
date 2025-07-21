from http.server import BaseHTTPRequestHandler, HTTPServer
import psycopg2

try:
    connection = psycopg2.connect(
        database='test_mydb',
        user='myuser',
        password='1234567',
        host='localhost',
        port='5432',
    )

    cursor = connection.cursor()
    print("db connected")

    cursor.execute("SELECT version();")
    db_version = cursor.fetchone()
    print("psql version",db_version)
except:
    print("db not connected")

class simpleHandler (BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type','text/plain')
            self.end_headers()
            self.wfile.write(b'Hello World!')
        elif self.path == '/hello':
            try:
                with open('index.html') as file:
                    content = file.read()
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                self.wfile.write(content.encode())
            except:
                self.send_response(500)
                self.send_header('Content-type','text/plain')
                self.end_headers()
                self.wfile.write(b'Internal Server Error')
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Route not found")

if __name__ == "__main__":
    server_address = ('',8080)
    httpd = HTTPServer(server_address,simpleHandler)
    print("Server is running on http://localhost:8000")
    httpd.serve_forever()