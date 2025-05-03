import os
import google.generativeai as genai
from google.api_core.exceptions import NotFound
from dotenv import load_dotenv

_ = load_dotenv()

api_key = os.getenv('GEMINI_API_KEY')
modelo = 'gemini-1.5-fflash'
genai.configure(api_key=api_key)

def carga_texto(archivo):
    try:
        with open(archivo,'r') as f:
            datos = f.read()
            return datos
    except IOError as e:
        print(f'Se generó un error al cargar el archivo. {e}')

def guarda_texto(archivo,contenido):
    try:
        with open(archivo,'w',encoding='utf-8') as f:
            f.write(contenido)            
    except IOError as e:
        print(f'Se generó un error al almacenar el archivo. {e}')   

def analizador_sentimiento(nombre_producto,modelo=modelo):
    prompt_sistema = """Eres un analista de sentimientos de opiniones de productos. 
                    Escribe un párrafo de hasta 50 palabras resumiendo las opiniones
                    y depués atribuye el sentimiento general frente al producto.
                    Identifica también 3 puntos fuertes y 3 puntos débiles 
                    identificados a partir de las opiniones de los clientes.

                    # Formato de salida

                    Nombre del Producto:
                    Resumen de las opiniones:
                    Sentimiento General: [Emplea solamente las opciones Positivo, Negativo, Neutro]
                    Puntos Fuerte: Lista con 3 bullets
                    Puntos Débiles: Lista con 3 bullets
                    """

    # nombre_producto = "camisetas"
    prompt_usuario = carga_texto(f'datos/reviews_{nombre_producto}.txt') 

    print(f'Iniciando el análisis de sentimiento del producto {nombre_producto}...')
    
    try:
        llm = genai.GenerativeModel(
                model_name = modelo,
                system_instruction=prompt_sistema
            )

        respuesta = llm.generate_content(prompt_usuario)

        texto_respuesta = respuesta.text

        guarda_texto(f'datos/sentimiento_sobre_{nombre_producto}.txt',texto_respuesta)
    except NotFound as e:
        modelo = os.getenv('GEMINI_MODELO_FLASH')
        print(f'El modelo no fue encontrado: {e}')
        analizador_sentimiento(nombre_producto,modelo)

def main():
    productos = ['camisetas','jeans','maquillaje']
    for producto in productos:
        analizador_sentimiento(producto)

if __name__=="__main__":
    main()