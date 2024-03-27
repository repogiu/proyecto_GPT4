# En views.py
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate, forms, get_user_model # importamos el método get_user_model
from django.contrib import messages
from .forms import UserRegisterForm


# pip install --upgrade django-crispy-forms

# Usar el método get_user_model garantiza que estás utilizando el modelo de usuario configurado en tu proyecto, ya sea el predeterminado de Django
# o tu modelo personalizado (UsuarioPersonalizado en tu caso).
User = get_user_model() # asignamos el modelo de usuario a la variable User
class Registro(View):
    # Metodos get para ofrecer el formulario
    def get(self, request):
        # Con esta clase creamos el formulario para crear usuarios
        form = UserRegisterForm()  # Usar el formulario personalizado
        return render(request, "registration/registro.html", {"form": form})

    # Metodo para enviar los datos a la BD
    def post(self, request):
        # form = UserCreationForm(request.POST)
        form = UserRegisterForm(request.POST)

        if form.is_valid():
            # Con esta instruccion se almacena el usuario en la base de datos
            usuario = form.save()

            # Funcion para que el usuario quede logueado luego que se registra
            login(request, usuario)

            return redirect("index")

        else:
            for mensaje in form.error_messages:
                messages.error(request, form.error_messages[mensaje])
            return render(request, "registration/registro.html", {"form": form})


'''
def cerrar_sesion(request):
    logout(request)

    return redirect("registro/login.html")
'''


def loguear(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            nombre_usuario = form.cleaned_data.get("username")
            contrasena = form.cleaned_data.get("password")
            # Validamos con el metodo authenticate
            usuario = authenticate(username=nombre_usuario, password=contrasena)
            if usuario is not None:
                login(request, usuario)
                return redirect("index")
            else:
                messages.error(request, "Usuario no válido")
        else:
            #messages.error(request, "Información incorrecta")
            for mensaje in form.error_messages:
                messages.error(request, form.error_messages[mensaje])
    form = AuthenticationForm()
    return render(request, "registration/login.html", {"form": form})



