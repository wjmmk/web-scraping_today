import string

def clean_text_fast(text):
    # 'string.punctuation' contiene: !"#$%&'()*+,-./:;<=>?@[\]^_`{|}~
    table = str.maketrans('', '', string.punctuation)
    return text.strip().lower().translate(table)

# Ejemplo:
print(clean_text_fast("¡Hola, Mundo! ¿Cómo estás?")) 
# Resultado: "hola mundo cómo estás"


import re

def clean_text_regex(text):
    # Convierte a minúsculas y quita espacios en los extremos
    text = text.lower().strip()
    # Elimina todo lo que NO sea una letra o espacio (incluye números y símbolos)
    text = re.sub(r'[^\w\s]', '', text)
    # Colapsa múltiples espacios en uno solo
    text = re.sub(r'\s+', ' ', text)
    return text

print(clean_text_regex("  Python es...   GENIAL!!!  "))
# Resultado: "python es genial"


import string
import re

def super_clean(text):
    # 1. Minúsculas y limpieza de bordes
    text = text.lower().strip()
    # 2. Quitar puntuación con translate (eficiencia)
    text = text.translate(str.maketrans('', '', string.punctuation))
    # 3. Limpiar espacios extra con regex
    text = re.sub(r'\s+', ' ', text)
    return text