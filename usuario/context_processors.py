# context_processors.py
# Finalmente, devuelve un diccionario con la información del crédito del usuario (creditos_usuario)
# para que esté disponible en todas las plantillas de tu aplicación, permitiendo el acceso a esta información
# en las vistas. Esto significa que en tus plantillas podrás utilizar {{ creditos_usuario }} para mostrar los créditos
# del usuario si está autenticado.
from .models import UsuarioPersonalizado


def creditos_usuario(request):
    usuario = request.user
    if usuario.is_authenticated:
        # Usar el campo 'creditos' en el modelo UsuarioPersonalizado para obtener los créditos del usuario
        creditos_usuario, creado = UsuarioPersonalizado.objects.get_or_create(id=usuario.id)
        return {'creditos_usuario': creditos_usuario}
    else:
        return {}
