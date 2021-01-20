from django.urls import path

from home import views

urlpatterns = [
    path("banner/", views.BannerAPIView.as_view()),
    path("head/", views.HeadAPIView.as_view()),
    path("foot/", views.FootAPIView.as_view()),
]