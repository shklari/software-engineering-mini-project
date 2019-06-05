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
    path('create_store/', LoginView.as_view(template_name='store/create_store.html'), name="create_store"),
    path('store/', LoginView.as_view(template_name='store/store.html'), name="store"),
    path('shop_all/', LoginView.as_view(template_name='store/shop_all.html'), name="shop_all"),
    path('single_product/', LoginView.as_view(template_name='store/single_product.html'), name="single_product"),
]+ static(settings.STATIC_ROOT, document_root=settings.STATIC_ROOT)
