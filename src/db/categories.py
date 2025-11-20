import uuid

def create_category(db, params):
    id = str(uuid.uuid4())
    categoria = params["categoria"]
    categoria_url = params["categoria_url"]
    sql = """
    INSERT INTO categorias (id, created_at, updated_at, categoria, categoria_url)
    VALUES (?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, ?, ?)
    """
    db.execute(
        sql, 
        [id, categoria, categoria_url]
    )
    db.commit()

    print(f"Categoria '{categoria}' criada com ID: {id}")
    return id    