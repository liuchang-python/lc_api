# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView, RetrieveAPIView

from course.models import CourseCategory, Course, CourseLesson, CourseChapter
from course.pagination import CoursePageNumberPagination
from course.serializer import CourseCategoryModelSerializer, CourseModelSerializer, CourseDetailModelSerializer, \
    CourseChapterModelSerializer


class CourseCategoryAPIVIew(ListAPIView):
    """课程分类信息查询"""
    queryset = CourseCategory.objects.filter(is_show=True, is_delete=False).order_by("-orders")
    serializer_class = CourseCategoryModelSerializer


class CourseAPIView(ListAPIView):
    """课程信息查询"""
    queryset = Course.objects.filter(is_show=True, is_delete=False).order_by("orders")
    serializer_class = CourseModelSerializer

    # 分类查询的模板类
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filter_fields = ("course_category",)

    # 排序
    ordering_fields = ("id", "students", "price")

    # 分页
    pagination_class = CoursePageNumberPagination


class LessonAPIView(RetrieveAPIView):
    """课程详情页"""

    queryset = Course.objects.filter(is_show=True, is_delete=False).order_by("orders")
    serializer_class = CourseDetailModelSerializer

    # 分类查询的模板类
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filter_fields = ("id",)


class CourseLessonAPIView(ListAPIView):
    queryset = CourseChapter.objects.filter(is_show=True, is_delete=False).order_by("orders")
    serializer_class = CourseChapterModelSerializer

    filter_backends = [DjangoFilterBackend]
    filter_fields = ("course",)