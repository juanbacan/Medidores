from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required

from medidores.models import CustomUser
from medidores.forms import ChangePasswordForm

from medidores.utils import enviar_correo_electronico_asincrono, generar_contrasena

@login_required
def change_password_view(request, *args, **kwargs):

    context = {}
    
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('password')

            usuario = request.user
            usuario.set_password(password)
            usuario.save()

            messages.success(request, 'Contraseña actualizada correctamente')
            return redirect('home')
        else:
            context['form'] = form
            return render(request, 'medidores/change_password.html', context)      
        
    else:
        form = ChangePasswordForm()
        context['form'] = form
        return render(request, 'medidores/change_password.html', context)
