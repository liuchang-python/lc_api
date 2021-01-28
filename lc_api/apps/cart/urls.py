from django.urls import path

from cart import views

urlpatterns = [
    path('option/', views.CartViewSet.as_view({'post': 'add_cart', "get": 'list_cart'})),
    path('change/', views.CartChangeViewSet.as_view({'post': 'change_selected'})),
    path('del/', views.CartDelViewSet.as_view({'post': 'del_cart'})),
]
