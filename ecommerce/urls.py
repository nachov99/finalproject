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
    path("product/<product_id>", views.product_single, name='product_single'),
    path("product/comment/<product_id>", views.comment, name="comment"),
    path("cart", views.cart, name='cart'),
    path('delete/<product_id>', views.delete_cart, name='delete_cart'),
    path('checkout', views.checkout, name='checkout'),
    path('category/<category_id>', views.categories, name='categories'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)