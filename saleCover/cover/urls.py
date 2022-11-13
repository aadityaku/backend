from django.urls import path
from .views import *
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_simplejwt.views import (TokenObtainPairView,TokenRefreshView)
urlpatterns = [ 
    path("",HomeView.as_view(),name="hello"),
    path("category/",CategoryView.as_view(),name="category"),
    path("subcategory/",SubCategoryView.as_view(),name="subcategory"),
    path("product/",ProductView.as_view(),name="product"),
    path("product/<slug>/",ProductView.as_view(),name="product"),
    path("add-to-cart/<slug>/",AddToCart.as_view(),name="add-to-cart"),
    path("my-order/",MyOrder.as_view(),name="myorder"),
    path("cart-list/",CartList.as_view(),name="cartlist"),
    path("minus-cart/<slug>/",MinusQtyFromCard.as_view(),name="minus-qty"),
    path("remove-product/<slug>/",RemoveProduct.as_view(),name="remove"),
    path('register-user/',Register.as_view(),name="register"),
    path('login/',TokenObtainPairView.as_view(),name="login"),
    path('login/refresh/',TokenRefreshView.as_view(),name="regresh"),
]
url_patterns=format_suffix_patterns(urlpatterns)