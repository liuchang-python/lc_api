from django.urls import path

from course import views

urlpatterns = [
    path("category/", views.CourseCategoryAPIVIew.as_view()),
    path("list/", views.CourseAPIView.as_view()),
    path("detail/<str:pk>",views.LessonAPIView.as_view()),
    path("chapter/",views.CourseLessonAPIView.as_view()),
]
