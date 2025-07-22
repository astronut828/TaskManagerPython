# routes/update.py
from conn import get_db_conn
from urllib.parse import urlparse, parse_qs, parse_qsl

def get_update_form(task_id):
    conn = get_db_conn()
    cur = conn.cursor()
    cur.execute("SELECT name, description FROM tasks WHERE id = %s", (task_id,))
    task = cur.fetchone()
    cur.close()
    conn.close()

    if not task:
        return "<h2>Task not found</h2>"

    name, desc = task

    with open("templates/update.html", "r") as f:
        template = f.read()
        template = template.replace("{{ID}}", task_id)
        template = template.replace("{{TITLE}}", name)
        template = template.replace("{{DESCRIPTION}}", desc)
        return template

def handle_update(request):
    query = parse_qs(urlparse(request.path).query)
    task_id = query.get("id", [None])[0]

    if request.command == "GET":
        return get_update_form(task_id)

    elif request.command == "POST":
        length = int(request.headers.get('Content-Length'))
        body = request.rfile.read(length).decode()
        data = dict(parse_qsl(body))
        name = data.get("name", "")
        desc = data.get("description", "")

        conn = get_db_conn()
        cur = conn.cursor()
        cur.execute("UPDATE tasks SET name=%s, description=%s WHERE id=%s", (name, desc, task_id))
        conn.commit()
        cur.close()
        conn.close()

        request.send_response(302)
        request.send_header("Location", "/")
        request.end_headers()
