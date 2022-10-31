from django.urls import path
from .views import *
urlpatterns = [
    path("",HomeView.as_view(),name="hello"),
    path("category/",CategoryView.as_view(),name="category"),
    path("subcategory/",SubCategoryView.as_view(),name="subcategory"),
    path("product/",ProductView.as_view(),name="product"),
    path("product/<slug>/",ProductView.as_view(),name="product"),
    path("add-to-cart/<slug>/",AddToCart.as_view(),name="add-to-cart"),
    path("my-order/",MyOrder.as_view(),name="myorder"),
    path("minus-cart/<slug>/",MinusQtyFromCard.as_view(),name="minus-qty"),
    path("remove-product/<slug>/",RemoveProduct.as_view(),name="remove"),
]
