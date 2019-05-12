from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    #path('', views.index, name='index'),
    path('login/', LoginView.as_view(template_name='accounts/sign_in.html'), name="login"),
    #path('signup/', LoginView.as_view(template_name='accounts/signup.html'), name="login"),
    path('signup/', views.signup, name="signup"),
]+ static(settings.STATIC_ROOT, document_root=settings.STATIC_ROOT)