from conn import get_db_conn
from urllib.parse import parse_qs

def handle_create(request):
    length = int(request.headers.get('Content-Length'))
    body = request.rfile.read(length).decode()
    data = parse_qs(body)
    title = data.get("name", [""])[0]
    desc = data.get("description", [""])[0]

    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute("INSERT INTO tasks (name, description) VALUES (%s, %s)", (title, desc))
    conn.commit()
    cur.close()
    conn.close()

    request.send_response(302)
    request.send_header("Location", "/")
    request.end_headers()
