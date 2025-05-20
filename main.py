import os
import google.generativeai as genai
from dotenv import load_dotenv

_ = load_dotenv()

api_key = os.getenv('GEMINI_API_KEY')
modelo_flash = os.getenv('GEMINI_MODELO_FLASH')

genai.configure(api_key=api_key)

prompt_sistema = "Únicamente debes generar una lista con los nombres de los productos y ofrece una breve descripción."

configuracion_modelo = {
    'temperature':0.5,
    'top_p':0.8,
    'top_k':64,
    'max_output_tokens':1024,
    'response_mime_type':'text/plain'
}

llm = genai.GenerativeModel(
    model_name=modelo_flash,
    system_instruction=prompt_sistema,
    generation_config=configuracion_modelo
)

pregunta = 'Lista 3 productos de moda sostenible para ir de compras.'

respuesta = llm.generate_content(pregunta)

print(f'La respuesta del modelo es:\n\n{respuesta.text}')