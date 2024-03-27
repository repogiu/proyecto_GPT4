#admin.py
from django.contrib import admin
from .models import Interest, Profile
from django.contrib.auth import get_user_model

User = get_user_model()

# Register your models here.
admin.site.register(Interest)
admin.site.register(Profile)


#personalizar cómo se muestran o se filtran los datos en la interfaz del panel de administración para un modelo
# específico (como Profile), puedes utilizar la técnica que te mencioné anteriormente, con @admin.register y
# ProfileAdmin para tener un mayor control sobre la apariencia y el filtrado de los datos en el panel de administración.
# @admin.register(Profile)
# class ProfileAdmin(admin.ModelAdmin):
#     # Define cómo se mostrarán los campos en el panel de administración
#     list_display = ('user', 'gender', 'date_of_birth', 'location')  # Ejemplo de campos a mostrar
#
#     def get_queryset(self, request):
#         qs = super().get_queryset(request)
#         # Si estás utilizando UsuarioPersonalizado, asegúrate de filtrar los perfiles por tu modelo de usuario personalizado
#         return qs.filter(user__isnull=False, user__instance_of=User)
