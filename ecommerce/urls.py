from django.urls import path
from django.conf.urls import url
from django.conf import settings

from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login", views.login_view, name="login_view"),
    path("register", views.register, name="register"),
    path("logout", views.logout_view, name="logout_view"),
    path("add/<product_id>", views.add_cart, name="add_cart"),
    path("category/<category_id>", views.category_products, name='category_products'),
    path("Orders", views.order_list, name="order_list"),
    path("addproduct", views.add_product, name="add_product"),
    #path("cart", views.cart, name='cart'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)