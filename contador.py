import os
import google.generativeai as genai
from dotenv import load_dotenv

_ = load_dotenv()

api_key = os.getenv('GEMINI_API_KEY')
modelo_flash = os.getenv('GEMINI_MODELO_FLASH')
modelo_pro = os.getenv('GEMINI_MODELO_PRO')

genai.configure(api_key=api_key)

costo_entrada_flash = 0.01
costo_salida_flash = 0.40
costo_entrada_pro = 1.25
costo_salida_pro = 10.00

modelo_flash = genai.get_model(f"models/{modelo_flash}")
modelo_pro = genai.get_model(f"models/{modelo_pro}")

limites_flash = {
    "tokens_entrada": modelo_flash.input_token_limit,
    "tokens_salida": modelo_flash.output_token_limit
}

limites_pro = {
    "tokens_entrada": modelo_pro.input_token_limit,
    "tokens_salida": modelo_pro.output_token_limit
}

print(f'Los límites del modelo flash 2.0: {limites_flash}\nLos límites del modelo pro 1.5: {limites_pro}')

modelo_flash = os.getenv('GEMINI_MODELO_FLASH')
modelo_pro = os.getenv('GEMINI_MODELO_PRO')

llm_flash = genai.GenerativeModel(f'models/{modelo_flash}')
llm_pro = genai.GenerativeModel(f'models/{modelo_pro}')

prompt_entrada = """Eres un especialista en moda sostenible y debes 
                   generar una lista de 20 prendas de vestir que se adapten 
                   a las últimas tendencias en este sector. Debes enfocar tu 
                   elección en confecciones que empleen materiales de 
                   alta calidad y durabilidad."""

ct_tokens_flash = llm_flash.count_tokens(prompt_entrada)
ct_tokens_pro = llm_pro.count_tokens(prompt_entrada)

print(f'La cantidad de tokens del modelo flash 2.0: {ct_tokens_flash}\nLa cantidad de tokens con el modelo pro 1.5: {ct_tokens_pro}')

def calculadora_costos(prompt,costo_entrada,costo_salida,modelo):
    respuesta = modelo.generate_content(prompt)
    tokens_entrada = respuesta.usage_metadata.prompt_token_count
    tokens_respuesta = respuesta.usage_metadata.candidates_token_count
    costo_total = ((tokens_entrada * costo_entrada) / 1e6) +  ((tokens_respuesta * costo_salida) / 1e6)
    return f'El costo total del modelo {modelo} es: {costo_total:.5f}'

flash = calculadora_costos(prompt_entrada,costo_entrada_flash,costo_salida_flash,llm_flash)
pro = calculadora_costos(prompt_entrada,costo_entrada_pro,costo_salida_pro,llm_pro)
print(flash,'\n',pro)