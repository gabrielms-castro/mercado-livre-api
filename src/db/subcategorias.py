import uuid
import sqlite3

def create_subcategoria(conn, cursor, category_id, params):
    id = str(uuid.uuid4())
    subcategoria = params["subcategoria"]
    subcategoria_url = params["subcategoria_url"]

    sql = """ 
    INSERT INTO subcategorias (id, created_at, updated_at, subcategoria, subcategoria_url, categoria_id)
    VALUES (?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, ?, ?, ?)
    """
    try:
        cursor.execute(
            sql,
            [id, subcategoria, subcategoria_url, category_id]
        )
        conn.commit()

        print(f"Subcategoria {subcategoria} criada")
        return id
    except sqlite3.IntegrityError as err:
        print(f"Subcategoria já existe: {err}")
        return None
    
def read_subcategory(cursor, subcategory_name, category_id):
    sql = """
    SELECT id, subcategoria, categoria_id
    FROM subcategorias
    WHERE subcategoria = ? AND categoria_id = ?
    """
    cursor.execute(sql, [subcategory_name, category_id])
    query = cursor.fetchone()
    if not query:
        return None
    return {
        "id": query[0],
        "subcategoria": query[1],
        "categoria_id": query[2],
    }

def list_all_subcategories(cursor):
    sql = """
    SELECT * 
    FROM subcategorias
    """
    cursor.execute(sql)
    query = cursor.fetchall()
    result = []
    for row in query:
        row_data = {}
        row_data['id'] = row[0]
        row_data['created_at'] = row[1]
        row_data['updated_at'] = row[2]
        row_data['subcategoria'] = row[3]
        row_data['subcategoria_url'] = row[4]
        row_data['categoria_id'] = row[5]
        result.append(row_data)

    return result