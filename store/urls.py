from django.urls import path
from . import views


urlpatterns = [
    path('', views.store, name="store"),
    path('category/<slug:category_slug>/', views.store, name="category"),
    path('cart/', views.cart, name="cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('update_item/', views.updateItem, name="update_item"),
    path('process_order/', views.processOrder, name="process_order"),
    path('product/<slug:product_slug>/', views.product_detail, name='product_detail'),]
