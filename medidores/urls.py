from django.urls import path

from .views import *

urlpatterns = [
    path('', home, name='home'),
    path('accounts/login/', login_view, name='login'),
    path('accounts/signup/', signup_view, name='signup'),
    path('logout/', logout_view, name='logout'),
    path('reset_password/', reset_password_view, name='resset_password'),
    path('change_password/', change_password_view, name='change_password'),
]
