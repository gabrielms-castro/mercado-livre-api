def brl_to_float(string):
    return float(string.replace("R$", "").replace(".", "").replace(",", "."))

def get_urls(data):
    if len(data) == 0:
        return None

    return [row['subcategoria_url'] for row in data]