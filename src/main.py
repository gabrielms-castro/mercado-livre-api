from src.db.db import DBConnectionHandler
from src.services.scraper import MercadoLivre

def main():
    db_handler = DBConnectionHandler()
    db_conn = db_handler.get_db_connection
    db_cursor = db_handler.get_cursor_object
    ml = MercadoLivre(db_conn, db_cursor)

    # print("Buscando categorias de produtos...")
    # ml.fetch_categorias()

    # print("Buscando subcategorias de produtos...")
    # ml.fetch_subcategorias()
    
    ml.crawl()

    print("Fechando conexão com banco de dados...")
    db_handler.close_connection()
    print("Finalizado!")

if __name__ == "__main__":
    main()