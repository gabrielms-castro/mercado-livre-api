import uuid

def create_subcategory(db, category_id, params):
    id = str(uuid.uuid4())
    subcategoria = params["subcategoria"]
    subcategoria_url = params["subcategoria_url"]

    sql = """ 
    INSERT INTO sub_categorias (id, created_at, updated_at, subcategoria, subcategoria_url, categoria_id)
    VALUES (?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, ?, ?, ?)
    """
    db.execute(
        sql,
        [id, subcategoria, subcategoria_url, category_id]
    )
    db.commit()

    print(f"Subcategoria {subcategoria} criada")
    return id
