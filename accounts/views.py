# views.py
'''
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User



def perfil(request, username):
    user = get_object_or_404(User, username=username)
    context = {
        'user': user
    }
    return render(request, 'perfil/perfil.html', context)
'''
#views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from django.views.generic.edit import UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile
from .forms import ProfileForm
import logging

User = get_user_model()


def perfil(request, username):
    user = get_object_or_404(User, username=username)
    context = {
        'user': user
    }
    return render(request, 'perfil/perfil.html', context)


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    logger = logging.getLogger(__name__)
    model = Profile
    form_class = ProfileForm
    template_name = 'perfil/profile_update.html'

    def get_object(self):
        return get_object_or_404(Profile, user=self.request.user)

    def get_form(self, form_class=None):
        # Pasamos la instancia del perfil al formulario
        form = super().get_form(form_class)
        form.instance = self.get_object()
        return form

    '''def get_form(self, form_class=None):
        # Pasamos la instancia del perfil al formulario
        form = super().get_form(form_class)
        form.instance = self.get_object()
        if self.request.method == 'POST':
            # Si el método es POST, pasamos el request.POST y el request.FILES
            form = ProfileForm(self.request.POST, self.request.FILES, instance=form.instance)
        elif self.request.method == 'GET':
            # Si el método es GET, pasamos el request.FILES
            form = ProfileForm(self.request.POST, self.request.FILES, instance=form.instance)
        return form'''



    '''def form_valid(self, form):
        # Asignamos el usuario actual al perfil
        form.instance.user = self.request.user
        # Guardamos el perfil
        form.save()
        # Hacemos el redirect con el username
        return redirect('perfil', username=self.request.user.username)'''

    def form_valid(self, form):
        # Asignamos el usuario actual al perfil
        form.instance.user = self.request.user

        # Verificamos si se proporcionó una nueva imagen en el formulario
        if 'image' in self.request.FILES:
            # Si se proporciona una nueva imagen, la guardamos en el perfil
            form.save()
        else:
            # Si no se proporciona una nueva imagen, guardamos el formulario sin cambiar la imagen de perfil
            form.save(commit=False)
            form.instance.image = self.get_object().image  # Asignamos la imagen actual del perfil al objeto del formulario
            form.save()

        # Hacemos el redirect con el username
        return redirect('perfil', username=self.request.user.username)



    def post(self, request, *args, **kwargs):
        # Obtenemos el formulario con el método POST
        form = self.get_form()
        form.instance = self.get_object()
        if form.is_valid():
            # Si el formulario es válido, lo procesamos
            return self.form_valid(form)
        else:
            # Si el formulario no es válido, lo volvemos a mostrar con los errores
            return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        # Obtenemos el contexto de la clase base
        context = super().get_context_data(**kwargs)
        # Agregamos el perfil que queremos actualizar al contexto
        context['profile'] = self.get_object()
        # Retornamos el contexto modificado
        return context







