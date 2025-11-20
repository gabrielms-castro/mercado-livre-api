import uuid

def create_category(conn, cursor, params):
    id = str(uuid.uuid4())
    categoria = params["categoria"]
    categoria_url = params["categoria_url"]
    sql = """
    INSERT INTO categorias (id, created_at, updated_at, categoria, categoria_url)
    VALUES (?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, ?, ?)
    """
    cursor.execute(
        sql, 
        [id, categoria, categoria_url]
    )
    conn.commit()

    print(f"Categoria '{categoria}' criada com ID: {id}")
    return id    

def read_category(cursor, category_name):
    sql = """
    SELECT id
    FROM categorias
    WHERE categoria = ?
    """
    cursor.execute(sql, [category_name])
    query = cursor.fetchone()
    if not query:
        return None
    return query[0]