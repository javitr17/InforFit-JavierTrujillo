from app.utils.openAI import get_openai_response


def preguntarIA(sitio, dias, duracion, nivel, objetivo):
    prompt=('Quiero que me muestres una rutina completa de entrenamiento en '+sitio+' para conseguir el objetivo de '+ objetivo+', sin calentamiento, '
            'para una persona con un nivel '+nivel+' que sea de '+dias+' dias a la semana y '+duracion+' de duración. Quiero que la respuesta'
            ' sea directamente el contenido que te he pedido, sin hacer referencias a la pregunta. El texto que me proporciones tiene '
            'que tener consideraciones. No quiero que aparezcan caracteres como este * en la respuesta. Ten en cuenta que la respuesta que me des'
            'la voy a usar en una vista de mi proyecto django para introducirla en un pdf mediante la libreria reportlab asi que debes darme la respuesta en un formato en el que se pueda '
            'introducir la respuesta en el pdf sin que el texto se entrecorte con el borde de la pagina u haya otros fallos')

    respuesta=get_openai_response(prompt)

    return respuesta