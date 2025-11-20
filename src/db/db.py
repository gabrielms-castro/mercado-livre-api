import sqlite3
from src.config import cfg

class DBConnectionHandler:
    def __init__(self):
        print("Conectando no Banco de Dados...")
        self._database_path = cfg.get('db_path')
        self._connection = None
        self._cursor = None

        self.connection_to_db()
        self.create_cursor_object()
        self.auto_migrate(self._connection, self._cursor)
    
    def connection_to_db(self):
        self._connection = sqlite3.connect(self._database_path)
    
    @property
    def get_db_connection(self):
        return self._connection

    def create_cursor_object(self):
        self._cursor = self._connection.cursor()

    @property
    def get_cursor_object(self):
        return self._cursor
    
    def close_connection(self):
        self._connection.close()
        self._connection = None
        self._cursor = None

    def auto_migrate(self, conn, cursor):
        print("Criando tabelas...")
        categorias = """
        CREATE TABLE IF NOT EXISTS categorias(
            id TEXT PRIMARY KEY,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            categoria TEXT NOT NULL UNIQUE,
            categoria_url TEXT NOT NULL
        )
        """
        cursor.execute(categorias)

        subcategorias = """
        CREATE TABLE IF NOT EXISTS subcategorias (
            id TEXT PRIMARY KEY,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            subcategoria TEXT NOT NULL,
            subcategoria_url TEXT NOT NULL,
            categoria_id TEXT NOT NULL,
            FOREIGN KEY (categoria_id) REFERENCES categorias(id),
            UNIQUE (subcategoria, categoria_id)
        )
        """
        conn.execute(subcategorias)

        produtos = """
        CREATE TABLE IF NOT EXISTS produtos (
            id TEXT PRIMARY KEY,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            produto TEXT NOT NULL,
            preco DOUBLE NOT NULL,
            descricao TEXT,
            produto_url TEXT NOT NULL,
            quantidade_vendas TEXT,
            avaliacao DOUBLE, 
            categoria_id TEXT,
            subcategoria_id TEXT,
            FOREIGN KEY (categoria_id) REFERENCES categorias(id),
            FOREIGN KEY (subcategoria_id) REFERENCES subcategorias(id)
        )
        """
        cursor.execute(produtos)

        conn.commit()
