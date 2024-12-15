from .models import Socio

def socio_imagen_context(request):
    socio_con_imagen = False
    url_imagen_socio = None

    if request.user.is_authenticated:
        try:
            socio = Socio.objects.get(user=request.user)
            if socio.imagen:  # Verificar si el socio tiene una imagen
                socio_con_imagen = True
                url_imagen_socio = socio.imagen.url  # Obtener la URL de la imagen
        except Socio.DoesNotExist:
            pass

    return {
        'socio_con_imagen': socio_con_imagen,
        'url_imagen_socio': url_imagen_socio,
    }
