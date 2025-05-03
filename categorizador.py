import os
import google.generativeai as genai
from dotenv import load_dotenv

_ = load_dotenv()

api_key = os.getenv('GEMINI_API_KEY')
modelo_flash = os.getenv('GEMINI_MODELO_FLASH')

genai.configure(api_key=api_key)

def categorizar_producto(pregunta,lista_categorias):
    prompt_sistema = f"""
    Eres un categorizador de productos. 
    Debes asumir las categorías presentes en la siguiente lista:

    # Lista de categorías válidas
    {lista_categorias.split(',')}

    # Formato de salida:
    Producto: Nombre del Producto.
    Categoría: Presenta la categoría del producto.

    # Ejemplo de salida:
    Producto: Cepillo eléctrico con recarga solar
    Categoría: Electrónicos Verdes
    """

    llm = genai.GenerativeModel(
        model_name=modelo_flash,
        system_instruction=prompt_sistema
    )

    respuesta = llm.generate_content(pregunta)

    return respuesta.text

def main():
    lista_categorias = 'Electrónicos Verdes, Moda Sostenible, Productos de Limpieza Ecológicos, Alimentos Orgánicos, Productos de Higiene Ecológicos'
    producto = input('Digita el producto que deseas clasificar: ')
    while producto != '':
        print(f'La respuesta del modelo es:\n\n{categorizar_producto(producto,lista_categorias)}')
        producto = input('Digita el producto que deseas clasificar') #Garantizamos que nuestro clasificador funcione siempre que haya una entrada del usuario

if __name__=="__main__":
    main()