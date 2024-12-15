from openai import OpenAI
from django.conf import settings
import re

def get_openai_response(prompt):
    api_key = settings.OPENAI_API_KEY
    print(F'KEY OPENAI: {api_key}')
    client = OpenAI(api_key= api_key)
    messages=[]
    messages.append({
        "role":"user",
        "content": prompt
    })

    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        stream=True,
    )
    respuesta_completa = ""

    # Recorre los fragmentos (chunks) del stream
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            respuesta_completa += chunk.choices[0].delta.content

    # Retorna la respuesta ensamblada
    respuesta_completa = clean_response(respuesta_completa)
    print(respuesta_completa)

    return respuesta_completa if respuesta_completa else "No se obtuvo respuesta."


def clean_response(text):
    # Eliminar caracteres no deseados (como asteriscos * y otros)
    text = re.sub(r'[^\w\s.,-]', '', text)  # Eliminar caracteres especiales
    text = re.sub(r'\*', '', text)  # Eliminar asteriscos
    return text