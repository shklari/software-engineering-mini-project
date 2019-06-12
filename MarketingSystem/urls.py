"""MarketingSystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
#from django.contrib.auth.views import LoginView
from django.contrib.auth.views import LoginView
from django.urls import path, include
# from django.contrib.auth.views import

from django.contrib.auth import views as auth_views

from . import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('shopping-cart/', LoginView.as_view(template_name='MarketingSystem/ShoppingCart.html'), name="shoppingCart"),
    path('add-new-owner/', LoginView.as_view(template_name='MarketingSystem/addNewOwner.html'), name="addNewOwner"),
    path('add-new-manager/', LoginView.as_view(template_name='MarketingSystem/addNewManager.html'), name="addNewManager"),
    path('remove-owner/', LoginView.as_view(template_name='MarketingSystem/removeOwner.html'), name="removeOwner"),
    path('remove-manager/', LoginView.as_view(template_name='MarketingSystem/removeManager.html'), name="removeManager"),
    path('add_product/', LoginView.as_view(template_name='store/add_product.html'), name="add_product"),
    path('edit_product/', LoginView.as_view(template_name='store/edit_product.html'), name="edit_product"),
    # path('', views.index, name='home'),
    path('', include('store.urls'), name='list'),
    path('', include('accounts.urls'), name='list'),
]

