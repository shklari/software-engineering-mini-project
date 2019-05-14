from django.urls import path

from . import views
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('', views.index, name='index'),
    path('create_store/', LoginView.as_view(template_name='store/create_store.html'), name="create_store"),
]