from django.urls import path

from store.views import genre_list
from . import views

urlpatterns = {
    path('', views, genre_list, name='genre_list')
}