# Store urls.py

from django.urls import path
from . import views
from Tshop import settings
from django.conf.urls.static import static


urlpatterns = [
    path('',views.index, name='index'),
    path('cart',views.cart),
    path('orders',views.orders, name='orders'),
    path('login',views.login, name='login'),
    path('signup',views.signup),
    path('logout',views.logout),
    path('checkout',views.checkout),
    path('validate_payment',views.validate_payment),
    path('products/<int:id>',views.show_products),
    path('addtocart/<int:id>/<str:size>',views.add_to_cart)
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
