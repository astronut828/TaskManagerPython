from conn import get_db_conn

def handle_fetch(handler):
    try:
        conn = get_db_conn()
        cur = conn.cursor()
        cur.execute("SELECT id, name, description FROM tasks ORDER BY id DESC")
        tasks = cur.fetchall()
        cur.close()
        conn.close()

        # Build the HTML content dynamically
        task_html = ""
        for task in tasks:
            id, name, description = task
            task_html += f"""
            <div class="task">
                <h2>{name}</h2>
                <p>{description}</p>
                <div class="actions">
                    <a href="/update?id={id}">Edit</a>
                    <a href="/delete?id={id}" onclick="return confirm('Delete this task?')">Delete</a>
                </div>
            </div>
            """

        # Load template and inject tasks
        with open('templates/index.html') as file:
            html = file.read()
            html = html.replace("{{TASKS}}", task_html)

        handler.send_response(200)
        handler.send_header("Content-type", "text/html")
        handler.end_headers()
        handler.wfile.write(html.encode())

    except Exception as e:
        print("Error in handle_fetch:", e)
        handler.send_response(500)
        handler.send_header("Content-type", "text/plain")
        handler.end_headers()
        handler.wfile.write(b"Internal server error")
