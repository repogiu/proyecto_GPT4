# En forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
# from django.contrib.auth.models import User
# from .models import UsuarioPersonalizado
from django.contrib.auth import get_user_model  # importamos el método get_user_model

User = get_user_model()  # asignamos el modelo de usuario a la variable User


# formulario personalizado que herede de UserCreationForm y que incluya los campos que quieras
#  los campos username, password1 y password2 que vienen por defecto
class UserRegisterForm(UserCreationForm):
    username = forms.CharField(max_length=150, required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'usuario123', "required": "required"}))
    first_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={"placeholder": "Juan", "required": "required"}))
    last_name = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={"placeholder": "Pérez", "required": "required"}))
    email = forms.EmailField(max_length=254, required=True,
                             widget=forms.TextInput(attrs={'placeholder': 'ejemplo@dominio.com', "required": "required"}))
    password1 = forms.CharField(max_length=128, required=True,
                                widget=forms.PasswordInput(
                                    attrs={"placeholder": "Contraseña123", "required": "required"}))
    password2 = forms.CharField(max_length=128, required=True,
                                widget=forms.PasswordInput(
                                    attrs={"placeholder": "Repite la contraseña", "required": "required"}))


    class Meta:
        model = User # usamos la variable User como modelo
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Nombre de usuario'
        self.fields['first_name'].label = 'Nombre'
        self.fields['last_name'].label = 'Apellido'
        self.fields['password1'].label = 'Contraseña'
        self.fields['password2'].label = 'Contraseña (confirmación)'

