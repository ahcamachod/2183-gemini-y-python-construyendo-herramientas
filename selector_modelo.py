import os
import google.generativeai as genai
from dotenv import load_dotenv

_ = load_dotenv()

api_key = os.getenv('GEMINI_API_KEY')
modelo = os.getenv('GEMINI_MODELO_FLASH')
genai.configure(api_key=api_key)

def carga_texto(archivo):
    try:
        with open(archivo,'r') as f:
            datos = f.read()
            return datos
    except IOError as e:
        print(f'Se generó un error al cargar el archivo. {e}')

prompt_sistema = """Identifica el perfil de compra para cada uno de los clientes.
                    El formato de salida debe ser:
                    Cliente - Describe el perfil con 3 palabras
                 """

prompt_usuario = carga_texto('lista_de_compras_100_clientes.csv')

llm = genai.GenerativeModel(model_name=modelo,system_instruction=prompt_sistema)

ct_tokens = llm.count_tokens(prompt_usuario)

limite_tokens = 3000

if ct_tokens.total_tokens >= limite_tokens:
    modelo = os.getenv('GEMINI_MODELO_PRO')

print(f'El modelo seleccionado es: {modelo}.')

llm = genai.GenerativeModel(model_name=modelo,system_instruction=prompt_sistema)

respuesta = llm.generate_content(prompt_usuario)

print(respuesta.text)