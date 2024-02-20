"""
URL configuration for ecommerce_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path
from ecommerce.views.orders import CartItemView, OrderItemView, OrderView, ShoppingCartView

from ecommerce.views.products import ProductViewApi


urlpatterns = [

    # Product url
    path('products', ProductViewApi.as_view(), name='products'),

    # cart urls
    path('shopping_cart/', ShoppingCartView.as_view(), name='shopping_cart'),
    path('cart_item/', CartItemView.as_view(), name='cart_item'),

    # order urls
    path('order/', OrderView.as_view(), name='order'),
    path('order_item/', OrderItemView.as_view(), name='order_item'),
]