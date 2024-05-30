"""Online_Shop_fin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from django.urls import path
from u_online_shop import views

urlpatterns = [
                  # MAIN
                  path('', views.homepage, name='homepage'),
                  path('admin/', admin.site.urls, name='admin_path'),
                  # SELLERS
                  path('become-seller/', views.become_seller, name='become_seller'),
                  path('seller_admin/', views.seller_admin, name='seller_admin'),
                  path('edit_seller/', views.edit_seller, name='edit_seller'),
                  path('sellers/', views.sellers, name='sellers'),
                  path('<int:seller_id>/', views.seller, name='seller'),
                  # CART
                  path('cart/', views.cart_detail, name='cart'),
                  path('success/', views.success, name='success'),
                  # PRODUCTS
                  path('search/', views.search, name='search'),
                  path('<slug:category_slug>/<slug:product_slug>/', views.product, name='product'),
                  path('add_product/', views.add_product, name='add_product'),
                  path('edit_product/<int:pk>/', views.edit_product, name='edit_product'),
                  # path('delete_product/<int:pk>/', views.delete_product, name='delete_product'),
                  # GENERAL FUNCTIONALITY
                  path('logout/', auth_views.LogoutView.as_view(), name='logout'),
                  path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
                  path('contact/', views.contact, name='contact'),
              ]
# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
