from django.urls import path
from django.contrib.auth import views as auth_views
from .views import Registro, logout, loguear

urlpatterns = [
   path('', Registro.as_view(), name="Usuario"),
   path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
   path('loguear', loguear, name="loguear"),

]
