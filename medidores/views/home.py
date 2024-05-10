

from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

from medidores.models import CustomUser, Medidor

@login_required
def home(request, *args, **kwargs):
    context = {}
    if request.method == 'POST':
        if request.POST.get('logout'):
            return redirect('logout')
        
    else:
        usuario = CustomUser.objects.get(pk=request.user.id)
        medidores = Medidor.objects.filter(cliente=usuario)
        context['medidores'] = medidores
        return render(request, 'medidores/home.html', context)

