import re
import random
import uuid

from rest_framework.views import APIView
from rest_framework.response import Response
from django_redis import get_redis_connection

from api import models
from utils.tencent.msg import send_message
from api.serializer.account import MessageSerializer,LoginSerializer

from django.shortcuts import render
from module import mqtt_function

class MessageView(APIView):
    def get(self,request,*args,**kwargs):
        """
        发送手机短信验证码
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        # 1.获取手机号
        # 2.手机格式校验
        ser = MessageSerializer(data=request.query_params)
        if not ser.is_valid():
            return Response({'status':False,'message':'手机格式错误'})
        phone = ser.validated_data.get('phone')

        # 3.生成随机验证码
        random_code = random.randint(1000,9999)
        # 5.把验证码+手机号保留（30s过期）
        """
        result = send_message(phone,random_code)
        if not result:
            return Response({"status": False, 'message': '短信发送失败'})
        """
        print(random_code)

        """
        #   5.1 搭建redis服务器（云redis）
        #   5.2 django中方便使用redis的模块 django-redis
               配置:
                    CACHES = {
                        "default": {
                            "BACKEND": "django_redis.cache.RedisCache",
                            "LOCATION": "redis://127.0.0.1:6379",
                            "OPTIONS": {
                                "CLIENT_CLASS": "django_redis.client.DefaultClient",
                                "CONNECTION_POOL_KWARGS": {"max_connections": 100}
                                # "PASSWORD": "密码",
                            }
                        }
                    }
                使用：
        """

        conn = get_redis_connection()
        conn.set(phone,random_code,ex=60)

        return Response({"status": True,'message':'发送成功'})


class LoginView(APIView):

    def post(self,request,*args,**kwargs):
        """
        1. 校验手机号是否合法
        2. 校验验证码，redis
            - 无验证码
            - 有验证码，输入错误
            - 有验证码，成功
        
        4. 将一些信息返回给小程序
        """
        ser = LoginSerializer(data=request.data)
        if not ser.is_valid():
            return Response({"status": False,'message':'验证码错误'})

        # 3. 去数据库中获取用户信息（获取/创建）
        phone = ser.validated_data.get('phone')
        user_object,flag = models.UserInfo.objects.get_or_create(phone=phone)
        user_object.token = str(uuid.uuid4())
        user_object.save()

        return Response({"status":True,"data":{"token":user_object.token,'phone':phone}})





def test(request):
     mqtt_function.mqtt_run()
     return render(request, 'test.html')
























