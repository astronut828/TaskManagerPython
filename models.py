from conn import get_db_conn


def create_tasks_table():
    conn = get_db_conn()
    cur = conn.cursor()

    create_table_sql = """
    CREATE TABLE IF NOT EXISTS tasks (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100) NOT NULL,
        description TEXT NOT NULL
    );
    """
    try:
        cur.execute(create_table_sql)
        conn.commit()
        print("Table 'tasks' created successfully!")
    except Exception as e:
        print("Failed to create table:", e)
        conn.rollback()
    finally:
        cur.close()
        conn.close()