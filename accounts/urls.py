from django.urls import path
from . import views
from .views import perfil, ProfileUpdateView


urlpatterns = [
    path('perfil/<str:username>/', views.perfil, name='perfil'),

    path('editar-perfil/', ProfileUpdateView.as_view(), name='editar_perfil'),

]