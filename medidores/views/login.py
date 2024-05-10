from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.core.mail import send_mail

from medidores.models import CustomUser
from medidores.forms import LoginForm

from medidores.utils import enviar_correo_electronico_asincrono

def login_view(request, *args, **kwargs):

    context = {}

    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(
                request,
                username =form.cleaned_data['cedula'],
                password=form.cleaned_data['password']
            )
            if user is not None:
                login(request, user)
                enviar_correo_electronico_asincrono(
                    'Inicio de Sesión',
                    'Se ha iniciado sesión en el sistema',
                    ['juan.ingaor@gmail.com']
                )
                return redirect('home')
            else:
                form.add_error(None, 'Cédula o contraseña incorrectos')
                context['form'] = form
                return render(request, 'medidores/login.html', context)
        else:
            context['form'] = form
            return render(request, 'medidores/login.html', context)
            
        
    else:
        form = LoginForm()
        context['form'] = form
        return render(request, 'medidores/login.html', context)
