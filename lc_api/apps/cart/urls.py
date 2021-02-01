from django.urls import path

from cart import views

urlpatterns = [
    path('option/', views.CartViewSet.as_view({'post': 'add_cart', "get": 'list_cart', "put": "change_expire"})),
    path('change/', views.CartChangeViewSet.as_view({'post': 'change_selected'})),
    path('del/', views.CartDelViewSet.as_view({'post': 'del_cart'})),
    path("order/", views.CartViewSet.as_view({"get": "get_select_course"})),
]
