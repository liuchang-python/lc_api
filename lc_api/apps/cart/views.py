from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from django_redis import get_redis_connection
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

from course.models import Course, CourseExpire
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
                # 'price': course.real_price,
                'price': course.expire_real_price(expire_id),
                # 当前课程的有效期
                "expire_text": course.expire_list,
            })

        return Response(data)

    def change_expire(self, request):
        """改变redis中的有效期"""
        user_id = request.user.id
        expire_id = request.data.get('expire_id')
        course_id = request.data.get('course_id')
        # print(expire_id, course_id)

        try:
            # 获取对应的课程信息
            course = Course.objects.get(is_delete=False, is_show=True, pk=course_id)

            # 判断前端传递的有效期选项 如果不是0 则修改课程对应有效期
            if expire_id > 0:
                expire_item = CourseExpire.objects.filter(is_show=True, is_delete=False, pk=expire_id)
                if not expire_item:
                    raise CourseExpire.DoesNotExist()

        except Course.DoesNotExist:
            return Response({"message": "课程信息不存在"}, status=status.HTTP_400_BAD_REQUEST)

        connection = get_redis_connection("cart")
        connection.hset("cart_%s" % user_id, course_id, expire_id)

        # TODO 重新计算切换有效期后的价格
        price = course.expire_real_price(expire_id)

        return Response({"message": "切换有效期成功","price":price})

    def get_select_course(self, request):
        """获取购物车中已勾选的课程并返回到前端"""
        user_id = request.user.id
        redis_connection = get_redis_connection('cart')

        # 获取当前购物车中的所有商品
        cart_list_byte = redis_connection.hgetall("cart_%s" % user_id)
        select_list_byte = redis_connection.smembers("selected_%s" % user_id)

        # 循环从mysql中获取课程的信息
        data = []
        total_price = 0  # 商品总价
        for course_id_byte, expire_id_byte in cart_list_byte.items():
            course_id = int(course_id_byte)
            expire_id = int(expire_id_byte)

            # 判断商品id是否在已勾选的商品列表中
            if course_id_byte in select_list_byte:
                try:
                    # 获取对应的课程信息
                    course = Course.objects.get(is_delete=False, is_show=True, pk=course_id)
                except Course.DoesNotExist:
                    continue

                # 如果有效期的id大于0，则代表需要重新计算商品的价格，有效期id不大于0，说明是原价
                original_price = course.price
                expire_text = "永久有效"

                try:
                    if expire_id > 0:
                        course_expire = CourseExpire.objects.get(id=expire_id)
                        # 对应有效期的价格
                        original_price = course_expire.price
                        expire_text = course_expire.expire_text
                except CourseExpire.DoesNotExist:
                    pass

                # 根据已勾选的商品对应有效期的价格去计算勾选商品的总价
                real_expire_price = course.expire_real_price(expire_id)

                # 将购物车中所需的信息返回
                data.append({
                    "course_img": IMG_SRC + course.course_img.url,
                    "name": course.name,
                    "id": course.id,
                    "expire_text": expire_text,
                    # 原价
                    "price": original_price,
                    # 活动 有效期计算后的真实价格
                    "real_price": "%.2f" % float(real_expire_price),
                    "discount_name": course.discount_name,
                })

                # 商品叠加后的总价
                total_price += float(real_expire_price)

        return Response({"course_list": data, "total_price": total_price, "message": "获取成功"})


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
