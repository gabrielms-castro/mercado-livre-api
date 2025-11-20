import sqlite3

def new_database(path_to_db):
    db = sqlite3.connect(path_to_db)
    auto_migrate(db)
    return db

def auto_migrate(db):
    categorias = """
    CREATE TABLE IF NOT EXISTS categorias(
        id TEXT PRIMARY KEY,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        categoria TEXT NOT NULL,
        categoria_url TEXT NOT NULL
    )
    """
    db.execute(categorias)

    sub_categorias = """
    CREATE TABLE IF NOT EXISTS sub_categorias (
        id TEXT PRIMARY KEY,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        subcategoria TEXT NOT NULL,
        subcategoria_url TEXT NOT NULL,
        categoria_id TEXT,
        FOREIGN KEY (categoria_id) REFERENCES categorias(id)
    )
    """
    db.execute(sub_categorias)
    db.commit()
