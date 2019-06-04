from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views
from django.contrib.auth.views import LoginView


from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_product/', LoginView.as_view(template_name='store/add_product.html'), name="add_product"),
    path('edit_product/', LoginView.as_view(template_name='store/edit_product.html'), name="edit_product"),
    path('store/', LoginView.as_view(template_name='store/store.html'), name="store"),
]+ static(settings.STATIC_ROOT, document_root=settings.STATIC_ROOT)
