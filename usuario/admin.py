'''
# Registramos el modelo de usuario
from django.contrib import admin

from usuario.models import UsuarioPersonalizado

# Registrar el modelo UsuarioPersonalizado
admin.site.register(UsuarioPersonalizado)
'''
# la clase UserAdmin para registrar tu modelo personalizado en el panel de administración
# permite aprovechar las funcionalidades que Django ofrece para el manejo de contraseñas, grupos, permisos
# y otras opciones del panel de administración

# admin.py
# Registramos el modelo de usuario
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin  # importamos la clase UserAdmin
from usuario.models import UsuarioPersonalizado


# subclase de UserAdmin: Agregar 'creditos' a los campos editables en el formulario del panel de administrador
class UsuarioPersonalizadoAdmin(UserAdmin):
    # Agregar 'historial' a los campos de solo lectura
    readonly_fields = ('historial',)
    # Agregar 'creditos' a la lista de campos que se mostrarán en el panel de administrador
    # list_display = ('creditos',)

    # Agregar 'creditos' a los campos editables en el formulario del panel de administrador
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('creditos', 'historial')}),
    )


# Registrar el modelo UsuarioPersonalizado usando la clase UserAdmin
# admin.site.register(UsuarioPersonalizado, UserAdmin) # pasamos la clase UserAdmin como segundo argumento
admin.site.register(UsuarioPersonalizado,
                    UsuarioPersonalizadoAdmin)  # pasamos clase personalizada UsuarioPersonalizadoAdmin como segundo argumento

# puedes crear una subclase de UserAdmin y personalizarla, por ejemplo, podrías cambiar los campos que se
# muestran al crear o editar un usuario, o añadir filtros o acciones personalizadas.
