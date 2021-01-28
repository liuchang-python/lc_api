import xadmin

from course import models
from course.models import CourseCategory, Course, CourseChapter, CourseLesson, Teacher


class CourseCategoryModelAdmin(object):
    """分类表"""
    pass


xadmin.site.register(CourseCategory, CourseCategoryModelAdmin)


class CourseModelAdmin(object):
    """课程表"""
    pass


xadmin.site.register(Course, CourseModelAdmin)


class CourseChapterModelAdmin(object):
    """章节表"""
    pass


xadmin.site.register(CourseChapter, CourseChapterModelAdmin)


class CourseLessonModelAdmin(object):
    """课时表"""
    pass


xadmin.site.register(CourseLesson, CourseLessonModelAdmin)


class TeacherModelAdmin(object):
    """讲师表"""
    pass


xadmin.site.register(Teacher, TeacherModelAdmin)


"""以下是课程活动相关的模型"""


class PriceDiscountTypeModelAdmin(object):
    """价格优惠类型"""
    pass


xadmin.site.register(models.CourseDiscountType, PriceDiscountTypeModelAdmin)


class PriceDiscountModelAdmin(object):
    """价格优惠公式"""
    pass


xadmin.site.register(models.CourseDiscount, PriceDiscountModelAdmin)


class CoursePriceDiscountModelAdmin(object):
    """商品优惠和活动的关系"""
    pass


xadmin.site.register(models.CoursePriceDiscount, CoursePriceDiscountModelAdmin)


class ActivityModelAdmin(object):
    """商品活动模型"""
    pass


xadmin.site.register(models.Activity, ActivityModelAdmin)

xadmin.site.register(models.CourseExpire)
