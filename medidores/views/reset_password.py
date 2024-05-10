from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.core.mail import send_mail

from medidores.models import CustomUser
from medidores.forms import ResetPasswordForm

from medidores.utils import enviar_correo_electronico_asincrono, generar_contrasena

def reset_password_view(request, *args, **kwargs):

    context = {}

    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = CustomUser.objects.filter(email=email).first()
            if user is not None:
                # Cambia la contraseña del usuario
                nueva_contraseña = generar_contrasena(10)
                user.set_password(nueva_contraseña)
                user.save()

                enviar_correo_electronico_asincrono(
                    'Restablecimiento de Contraseña',
                    'Se ha solicitado un restablecimiento de contraseña. Su nueva contraseña es: {}'.format(nueva_contraseña),
                    [user.email]
                )
                messages.success(request, 'Se ha enviado un correo electrónico con las instrucciones para restablecer la contraseña')
                return redirect('login')
            else:
                form.add_error(None, 'No se ha encontrado un usuario con el email proporcionada')
                context['form'] = form
                return render(request, 'medidores/reset_password.html', context)
        else:
            context['form'] = form
            return render(request, 'medidores/reset_password.html', context)      
        
    else:
        form = ResetPasswordForm()
        context['form'] = form
        return render(request, 'medidores/reset_password.html', context)
