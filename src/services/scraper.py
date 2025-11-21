
import httpx
from selectolax.parser import HTMLParser
from src.config import cfg
from src.db.categorias import create_category, read_category
from src.db.produtos import create_product_metada
from src.db.subcategorias import create_subcategoria, read_subcategory
from src.utils import brl_to_float


class MercadoLivre:
    def __init__(self, db_conn, db_cursor):
        self.db_conn = db_conn
        self.db_cursor = db_cursor
        self.base_url = "https://www.mercadolivre.com.br"
        self.headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
        }

    def _extract_text(self, html, selector):
        try:
            return html.css_first(selector).text()
        except AttributeError:
            return None

    def _extract_href(self, html, selector):
        try:
            return html.css_first(selector).attributes.get('href')
        except AttributeError:
            return None

    def fetch_categorias(self, endpoint="/categorias"):
        url = f"{self.base_url}{endpoint}"
        response = httpx.get(
            url=url,
            headers=self.headers
        )

        if response.status_code != 200:
            raise Exception(f"Error fetching {url}")
        
        html = HTMLParser(response.text)

        categorias = html.css("div.categories__container")
        
        for categoria in categorias:
            categoria_nome = self._extract_text(categoria, 'h2.categories__title')
            categoria_url = self._extract_href(categoria, 'h2.categories__title a')
            
            query = read_category(self.db_cursor, categoria_nome)
            if query:
                print(f"Categoria já existe: {categoria_nome}")
                continue            
            
            item = {
                "categoria": categoria_nome,
                "categoria_url": categoria_url
            }
            create_category(self.db_conn, self.db_cursor, item)

    def fetch_subcategorias(self, endpoint="/categorias"):
        url = f"{self.base_url}{endpoint}"
        response = httpx.get(
            url=url,
            headers=self.headers
        )

        if response.status_code != 200:
            raise Exception(f"Error fetching {url}")
        
        html = HTMLParser(response.text)

        categorias = html.css("div.categories__container")
        
        for categoria in categorias:
            categoria_nome = self._extract_text(categoria, 'h2.categories__title')
            categoria_id = read_category(self.db_cursor, categoria_nome)

            categoria_ul = categoria.css('ul.categories__list')
            for subcategorias in categoria_ul:
                subcategorias_li = subcategorias.css("li")
                for subcategoria in subcategorias_li:
                    subcategoria_nome = self._extract_text(subcategoria, 'a h3')
                    subcategoria_url = self._extract_href(subcategoria, 'a')

                    query = read_subcategory(self.db_cursor, subcategoria_nome, categoria_id)
                    if query:
                        print(f"Subcategoria já existe: {subcategoria_nome}")
                        continue                    

                    item = {
                        "subcategoria": subcategoria_nome,
                        "subcategoria_url": subcategoria_url
                    }
                    create_subcategoria(
                        self.db_conn,
                        self.db_cursor,
                        categoria_id,
                        item
                    )
    
    def fetch_products(self):
        response = httpx.get(
            url="https://lista.mercadolivre.com.br/espelho-retrovisor-com-camera#trends_tracking_id=137f4f41-08a3-4601-badb-c9eaa36c11bd&component_id=MOST_WANTED",
            headers=self.headers
        )
        html = HTMLParser(response.text)
        cards = html.css('div.poly-card__content')
        for card in cards:
            produto_titulo = self._extract_text(card, 'h3 a')
            produto_url = self._extract_href(card, 'h3 a')
            preco = self._extract_text(card, 'div.poly-price__current span.andes-money-amount--cents-superscript')
            preco_cleaned = brl_to_float(preco)
            item = {
                "produto": produto_titulo,
                "produto_url": produto_url,
                "preco": preco_cleaned
            }
            print(item)
            create_product_metada(self.db_conn, self.db_cursor, item)