# forms.py
from django import forms
from .models import Profile, Interest
from datetime import datetime



class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'gender', 'date_of_birth', 'location', 'bio']
        widgets = {
            #'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            #'date_of_birth': forms.SelectDateWidget(),
            'date_of_birth': forms.SelectDateWidget(
                years=range(datetime.now().year - 100, datetime.now().year + 5)
            ),
            #'interests': forms.CheckboxSelectMultiple(),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            #'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),

            #'image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),


        }
        help_texts = {
            #'image': 'Sube una imagen para tu perfil',
            #'gender': 'Selecciona tu género o deja el campo en blanco si prefieres no decirlo',
            'location': 'Ingresa tu ciudad o país de residencia',
            'bio': 'Escribe una breve descripción sobre ti',
            #'interests': 'Selecciona los temas que te interesan'
        }
        labels = {
            'image': 'Imagen de perfil',
            'gender': 'Género',
            'date_of_birth': 'Fecha de nacimiento',
            'location': 'Ubicación',
            'bio': 'Biografía',
            #'interests': 'Intereses'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['image'].required = False  # Hacer que el campo image no sea obligatorio
        self.fields['bio'].max_length = 200  # Cambiar el máximo de caracteres del campo bio
        self.fields['gender'].required = False
        self.fields['location'].required = False
        self.fields['date_of_birth'].required = False


