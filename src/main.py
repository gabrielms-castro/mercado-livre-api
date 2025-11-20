
import requests
from bs4 import BeautifulSoup
import src.config as config
from src.db.categories import create_category
from src.db.sub_categories import create_subcategory

def main():
    db = config.cfg['db']

    url = "https://www.mercadolivre.com.br/categorias"
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
    }

    response = requests.get(
        url=url, 
        headers=headers
    )

    html = response.text
    soup = BeautifulSoup(html, 'lxml')
    categories = soup.find_all('div', class_='categories__container')
    for category in categories:
        params = {
            'categoria': category.h2.text,
            'categoria_url': category.h2.a['href']
        }
        category_id = create_category(db, params)

        for sub_category in category.ul:
            subcategory_params = {
                'subcategoria': sub_category.h3.text,
                'subcategoria_url': sub_category.a['href']
            }
            subcategory_id = create_subcategory(
                db, 
                category_id=category_id, 
                params=subcategory_params 
            )

if __name__ == "__main__":
    main()