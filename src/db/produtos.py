import uuid

def create_product_metada(conn, cursor, params):
    id = str(uuid.uuid4())
    produto = params["produto"]
    produto_url = params["produto_url"]
    preco = params["preco"]

    sql = """ 
    INSERT INTO produtos (id, created_at, updated_at, produto, produto_url, preco)
    VALUES (?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, ?, ?, ?)
    """
    cursor.execute(
        sql,
        [id, produto, produto_url, preco]
    )
    conn.commit()

    print(f"Produto {produto} criada")
    return id
