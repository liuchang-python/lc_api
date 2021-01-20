from django.shortcuts import render

# Create your views here.
from rest_framework.generics import ListAPIView

from home.models import Banner, Nav
from home.serializer import BannerModelSerializer, NavModelSerializer


class BannerAPIView(ListAPIView):
    """轮播图接口"""
    queryset = Banner.objects.filter(is_show=True, is_delete=False).order_by("-orders")
    serializer_class = BannerModelSerializer


class FootAPIView(ListAPIView):
    """脚部链接"""
    queryset = Nav.objects.filter(is_delete=False, is_show=True, position=2).order_by("-orders")
    serializer_class = NavModelSerializer


class HeadAPIView(ListAPIView):
    """头部链接"""
    queryset = Nav.objects.filter(is_delete=False, is_show=True, position=1).order_by("orders")
    serializer_class = NavModelSerializer
