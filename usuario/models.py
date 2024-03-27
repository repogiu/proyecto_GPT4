# models.py
import datetime
from ProyectoTikTok import settings
from django.db import models
# Importar la clase AbstractUser en lugar de User
from django.contrib.auth.models import AbstractUser


# Crear una clase que herede de AbstractUser y añadir el campo creditos
class UsuarioPersonalizado(AbstractUser):
    creditos = models.PositiveIntegerField(verbose_name='creditos',
                                           default=10,
                                           blank=True, # permite que el campo se deje en blanco al validar los formularios, pero no afecta a la base de datos
                                           null=True, ) # admite valores nulo
    historial = models.TextField(verbose_name='historial', blank=True, null=True)

    def restar_credito(self):
        from datetime import datetime  # Importación en la función
        # Restar un crédito al usuario
        self.creditos -= 1

        # Asegurar que historial no sea None
        if self.historial is None:
            self.historial = ""

        # Actualizar el historial con la fecha y hora del descuento
        fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.historial += f"\n-1 crédito el {fecha}"
        # Guardar los cambios en la base de datos
        self.save()

    def __str__(self):
        return f"Creditos de {self.username}: {self.creditos}"

# Eliminar la clase CreditosUsuario, ya que no es necesaria
# Si quieres mantener el campo historial, puedes añadirlo al modelo UsuarioPersonalizado