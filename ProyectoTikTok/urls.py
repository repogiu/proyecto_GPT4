"""
URL configuration for ProyectoTikTok project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from video_tiktok.views import index
from video_tiktok import views
from django.conf import settings  # Importar settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views as auth_views # contraseñas


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    #path('index/', views.index, name='index'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('generate_script/', views.generate_script, name='generate_script'),
    # la función include de Django, que te permite incluir las rutas definidas en otro archivo urls.py
    path('usuario/', include('usuario.urls')),
    path('accounts/', include('accounts.urls')),




]


if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)



# settings.py
#LOGIN_REDIRECT_URL = 'video_tiktok/index/'
#LOGIN_URL = 'registro/'


# Esto es solo necesario cuando DEBUG = True:
# Django agregará las rutas para servir los archivos estáticos automáticamente
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
