from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from django_redis import get_redis_connection
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from course.models import Course
from lc_api.settings.constants import IMG_SRC


class CartViewSet(ViewSet):
    """购物车视图"""
    # 只有登录且认证的用户才可以访问
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]

    def add_cart(self, request):
        """
        将课程添加至购物车
        :param request: 用户id 课程ID 勾选状态 有效期
        :return:
        """
        course_id = request.data.get('course_id')
        # 当前视图只允许经过认证的用户访问，如果用户通过认证，则用户的信息会保存在request模块中的user
        user_id = request.user.id
        # 是否勾选
        select = True
        # 有效期
        expire = 0
        # 校验前端传递的参数
        try:
            Course.objects.get(is_show=True, is_delete=False, pk=course_id)
        except Course.DoesNotExist:
            return Response({'message': '参数有误，课程不存在'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            redis_connection = get_redis_connection('cart')
            # 多次操作Redis建议使用管道，节省Redis的开销
            pipeline = redis_connection.pipeline()
            # 开启管道
            pipeline.multi()
            # 保存商品信息以及对应的有效期  hash
            pipeline.hset("cart_%s" % user_id, course_id, expire)
            # 保存商品的勾选状态 set
            pipeline.sadd("selected_%s" % user_id, course_id)
            # 执行
            pipeline.execute()

            # 获取购物车中的商品数量
            cart_len = redis_connection.hlen('cart_%s' % user_id)
        except:
            return Response({"message": "参数有误，购物车添加失败"}, status=status.HTTP_507_INSUFFICIENT_STORAGE)

        return Response({"message": "购物车添加成功", 'cart_length': cart_len})

    def list_cart(self, request):
        """展示购物车"""
        user_id = request.user.id
        redis_connection = get_redis_connection('cart')
        cart_list_byte = redis_connection.hgetall("cart_%s" % user_id)
        select_list_byte = redis_connection.smembers("selected_%s" % user_id)

        # 循环从MySQL中获取课程的信息
        data = []
        for course_id_byte, expire_id_byte in cart_list_byte.items():
            course_id = int(course_id_byte)
            expire_id = int(expire_id_byte)

            try:
                # 获取对应的课程信息
                course = Course.objects.get(is_show=True, is_delete=False, pk=course_id)
            except Course.DoesNotExist:
                continue

                # 将购物车所需信息返回
            data.append({
                'selected': True if course_id_byte in select_list_byte else False,
                'course_image': IMG_SRC + course.course_img.url,
                'name': course.name,
                'id': course.id,
                'expire_id': expire_id,
                'price': course.price,
            })

        return Response(data)

class CartChangeViewSet(ViewSet):
    # 只有登录且认证的用户才可以访问
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    def change_selected(self, request):
        """修改勾选状态"""

        user_id = request.user.id
        course_id = request.data.get('course_id')
        select = request.data.get('select')
        redis_connection = get_redis_connection('cart')
        try:
            if select:
                redis_connection.sadd("selected_%s" % user_id, course_id)
            else:
                redis_connection.srem("selected_%s" % user_id, course_id)
        except:
            return Response({'message':'不存在'},status=status.HTTP_400_BAD_REQUEST)
        return Response({'message':'成功'})


class CartDelViewSet(ViewSet):
    # 只有登录且认证的用户才可以访问
    permission_classes = [IsAuthenticated]
    authentication_classes = [JSONWebTokenAuthentication]
    def del_cart(self, request):
        user_id = request.user.id
        course_id = request.data.get('course_id')
        redis_connection = get_redis_connection('cart')
        try:
            redis_connection.hdel("cart_%s" % user_id,course_id)
            redis_connection.srem("selected_%s" % user_id, course_id)
        except:
            return Response({'message':'不存在'},status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': '成功'})
