

from django.shortcuts import redirect, render
from django.contrib.auth import logout

def logout_view(request, *args, **kwargs):
    if request.user.is_authenticated:
        logout(request)
        return redirect('login')
    else:
        return redirect('login')
