# routes/delete.py
from conn import get_db_conn
from urllib.parse import urlparse, parse_qs

def handle_delete(request):
    query = parse_qs(urlparse(request.path).query)
    task_id = query.get("id", [None])[0]

    if task_id:
        conn = get_db_conn()
        cur = conn.cursor()
        cur.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
        conn.commit()
        cur.close()
        conn.close()

    request.send_response(302)
    request.send_header("Location", "/")
    request.end_headers()
