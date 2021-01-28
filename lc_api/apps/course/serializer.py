from rest_framework.serializers import ModelSerializer

from course.models import CourseCategory, Course, Teacher, CourseLesson, CourseChapter


class CourseCategoryModelSerializer(ModelSerializer):
    """分类"""

    class Meta:
        model = CourseCategory
        fields = ['id', "name"]


class TeacherModelSerializer(ModelSerializer):
    class Meta:
        model = Teacher
        fields = ['id', "name", "title", "image", "signature", "brief"]


class CourseModelSerializer(ModelSerializer):
    """课程列表"""

    # 返回课程列表所需的老师的信息
    teacher = TeacherModelSerializer()

    class Meta:
        model = Course
        fields = ["id", "name", "course_img", "students", "lessons", "pub_lessons", "price", "teacher", 'lesson_list']


class CourseDetailModelSerializer(ModelSerializer):
    """课程详情"""
    teacher = TeacherModelSerializer()

    class Meta:
        model = Course
        fields = ["id", "name", "level_name", "course_img", "students", "lessons",
                  "pub_lessons", "price", "teacher", 'course_video',"brief_html"]


class CourseLessonModelSerializer(ModelSerializer):
    """课时序列化器"""
    class Meta:
        model = CourseLesson
        fields = ["id", "name", "free_trail"]


class CourseChapterModelSerializer(ModelSerializer):
    """章节序列化器"""
    coursesections = CourseLessonModelSerializer(many=True)

    class Meta:
        model = CourseChapter
        fields = ['id', 'name', 'chapter', 'coursesections']
