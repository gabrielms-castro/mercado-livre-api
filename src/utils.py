def brl_to_float(string):
    return float(string.replace("R$", "").replace(".", "").replace(",", "."))