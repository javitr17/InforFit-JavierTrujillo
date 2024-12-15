from app.utils.openAI import get_openai_response


def preguntarIA(sitio, dias, duracion, nivel, objetivo):
    prompt=('Quiero que me muestres una rutina completa de entrenamiento en '+sitio+' para conseguir el objetivo de '+ objetivo+', sin calentamiento, '
            'para una persona con un nivel '+nivel+' que sea de '+dias+' dias a la semana y '+duracion+' de duración. Quiero que la respuesta'
            ' sea directamente el contenido que te he pedido, sin hacer referencias a la pregunta. El texto que me proporciones tiene '
            'que tener consideraciones. No quiero que aparezcan caracteres como este * en la respuesta. En cuanto al formato del texto de la respuesta que me des quiero que en cada línea haya como máximo 14 palabras')

    respuesta=get_openai_response(prompt)

    return respuesta