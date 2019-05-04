from django.urls import path

from . import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    #path('', views.index, name='index'),
    path('login/', LoginView.as_view(template_name='accounts/login.html'), name="login"),
    path('signup/', LoginView.as_view(template_name='accounts/signup.html'), name="login"),
]