
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login

from medidores.models import CustomUser

from medidores.forms import SignupForm

def signup_view(request, *args, **kwargs):
    context = {}
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            cedula = form.cleaned_data['cedula']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            fecha_nacimiento = form.cleaned_data['fecha_nacimiento']
            celular = form.cleaned_data['celular']
            password = form.cleaned_data['password']

            if CustomUser.objects.filter(cedula=cedula).exists():
                form.add_error('cedula', 'La cédula ya está registrada')
                context['form'] = form
                return render(request, 'medidores/signup.html', context)
            
            if CustomUser.objects.filter(email=email).exists():
                form.add_error('email', 'El correo electrónico ya está registrado')
                context['form'] = form
                return render(request, 'medidores/signup.html', context)

            user = CustomUser.objects.create_user(
                username=cedula,
                email=email,
                password=password,
                cedula=cedula,
                first_name=first_name,
                last_name=last_name,
                fecha_nacimiento=fecha_nacimiento,
                celular=celular
            )

            login(request, user)
            return redirect('home')
        else:
            context['form'] = form
            return render(request, 'medidores/signup.html', context)
        
    else:
        form = SignupForm()
        context['form'] = form
        return render(request, 'medidores/signup.html', context)

