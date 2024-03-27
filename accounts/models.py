#models.py
#from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from ProyectoTikTok import settings
from django.contrib.auth import get_user_model  # Importa get_user_model

User = get_user_model()  # Asigna el modelo de usuario a la variable User


# Create your models here.
# Modelo de Intereses
class Interest(models.Model):
    name = models.CharField(max_length=80, unique=True, verbose_name='Nombre')

    class Meta:
        verbose_name = 'Interés'
        verbose_name_plural = 'Intereses'
        ordering = ['name']

    def __str__(self):
        return self.name


GENDER_CHOICES = (('F', 'Femenino'), ('M', 'Masculino'), ('NB', 'No binario'), ('O', 'Otro'),)


class Profile(models.Model):
    #user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    image = models.ImageField(default='users/perfil-del-usuario.png', upload_to='users/')
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, null=True, blank=True, verbose_name='Género')
    date_of_birth = models.DateField(null=True, blank=True, verbose_name='Fecha de nacimiento')
    location = models.CharField(max_length=80, null=True, blank=True)
    bio = models.TextField(max_length=400, null=True, blank=True)
    interests = models.ManyToManyField(Interest, verbose_name='Intereses')

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'
        ordering = ['-id']


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


def save_user_profile(sender, instance, created, **kwargs):
    instance.profile.save()


post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)
