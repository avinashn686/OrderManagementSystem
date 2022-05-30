import logging
from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User, Group
from oms.models import Order
from oms.serializers import OrderCreateSerializer, OrderListSerializer
from rest_framework import viewsets
from rest_framework import permissions
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from oms.models import User,Product
from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     RetrieveUpdateAPIView)
from rest_framework.exceptions import APIException, NotFound
from oms.serializers import UserSerializer, UserLoginSerializer, UserLogoutSerializer,ProductCreateSerializer,ProductListSerializer
from django.contrib.auth.decorators import login_required
logger = logging.getLogger(__name__)

class Record(generics.ListCreateAPIView):
    # get method handler
    queryset = User.objects.all()
    serializer_class = UserSerializer


class Login(generics.GenericAPIView):
    # get method handler
    queryset = User.objects.all()
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer_class = UserLoginSerializer(data=request.data)
        if serializer_class.is_valid(raise_exception=True):
            return Response(serializer_class.data, status=HTTP_200_OK)
        return Response(serializer_class.errors, status=HTTP_400_BAD_REQUEST)

class Logout(generics.GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserLogoutSerializer

    def post(self, request, *args, **kwargs):
        serializer_class = UserLogoutSerializer(data=request.data)
        if serializer_class.is_valid(raise_exception=True):
            return Response(serializer_class.data, status=HTTP_200_OK)
        return Response(serializer_class.errors, status=HTTP_400_BAD_REQUEST)


class ProductCreateView(CreateAPIView):
    serializer_class = ProductCreateSerializer

    def perform_create(self, serializer):
        data = {}
        try:
            if serializer.is_valid():
                project = serializer.save()
                data["status"] = "success"
                data["message"] = "created successfully"
                data["code"] = 201
            else:
                data["message"] = "create Failed"
                data["details"] = serializer.errors
                data["status"] = "failed"
                data["code"] = 422
        except Exception as exception:
            logger.exception("Something went wrong %s", exception)
            data["status"] = "failed"
            data["message"] = "something_went_wrong"
            data["code"] = 500
        return data

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        data = self.perform_create(serializer)
        http_code = data.pop('code',None)
        return Response(data=data, status=http_code)


class ProducteditView(RetrieveUpdateAPIView):
    serializer_class = ProductCreateSerializer
    queryset = Product.objects.order_by("id").all()
    lookup_field = "object_id"

    def perform_update(self, serializer):
        data = {}
        try:
            if serializer.is_valid():
                project = serializer.save()   
                data["message"] = "updated successfully"
                data["status"] = "success"
                data['code'] = 200
        except Exception as exception:
            logger.exception("Something went wrong %s", exception)
            data["status"] = "failed"
            data["message"] ='something_went_wrong'
            data['code'] = 500
        return data
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance,data=request.data)
        data = self.perform_update(serializer)
        http_code = data.pop('code',None)
        return Response(data=data, status=http_code)

class ProductListView(ListAPIView):

    serializer_class = ProductListSerializer

    # overriding the method

    def get_queryset(self, *args, **kwargs):
        queryset_list = list()
        queryset_list=Product.objects.all()

        return queryset_list
# @login_required()
class OrderCreateView(CreateAPIView):
    serializer_class = OrderCreateSerializer

    def perform_create(self, serializer):
        data = {}
        try:
            if serializer.is_valid():
                user_id=self.request.data.get('user_id')
                usertype=User.objects.get(id=user_id)
                if usertype.user_type == 'consumer':
                    project = serializer.save()
                    data["status"] = "success"
                    data["message"] = "created successfully"
                    data["code"] = 201
                else:
                    data["message"] = "not consumer user"
                    data["status"] = "failed"
                    data["code"] = 422
            else:
                data["message"] = "create Failed"
                data["details"] = serializer.errors
                data["status"] = "failed"
                data["code"] = 422
        except Exception as exception:
            logger.exception("Something went wrong %s", exception)
            data["status"] = "failed"
            data["message"] = "something_went_wrong"
            data["code"] = 500
        return data

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        data = self.perform_create(serializer)
        http_code = data.pop('code',None)
        return Response(data=data, status=http_code)


class OrdereditView(RetrieveUpdateAPIView):
    serializer_class = OrderCreateSerializer
    queryset = Order.objects.order_by("id").all()
    lookup_field = "object_id"

    def perform_update(self, serializer):
        data = {}
        try:
            if serializer.is_valid():
                user_id=self.request.data.get('user_id')
                usertype=User.objects.get(id=user_id)
                if usertype.user_type == 'consumer':
                    project = serializer.save()   
                    data["message"] = "updated successfully"
                    data["status"] = "success"
                    data['code'] = 200
                else:
                    data["message"] = "not consumer user"
                    data["status"] = "failed"
                    data["code"] = 422
        except Exception as exception:
            logger.exception("Something went wrong %s", exception)
            data["status"] = "failed"
            data["message"] ='something_went_wrong'
            data['code'] = 500
        return data
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance,data=request.data)
        data = self.perform_update(serializer)
        http_code = data.pop('code',None)
        return Response(data=data, status=http_code)

class OrderListView(ListAPIView):

    serializer_class = OrderListSerializer

    def get_queryset(self, *args, **kwargs):
        queryset_list = list()
        queryset_list=Order.objects.all()

        return queryset_list

class OrderDestroyView(DestroyAPIView):
    """
    Order Delete API View
    """
    queryset = Order.objects.order_by("id").all()
    serializer_class = OrderListSerializer
    lookup_field = "object_id"

    def perform_destroy(self, instance):
        data = {}
        try:
            object_id = self.kwargs.get("object_id")
            order_obj = Order.objects.get(object_id=object_id)

            order_obj.delete()
            data["status"] = True
            data["message"] = "deleted"
            data["code"] = 200

        except Exception as exception:
            logger.exception("Exception occuring while fetching Request %s", exception)
            data["message"] = "something_went_wrong"
            data["status"] = "failed"
            data["code"] = 500
        return data

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        data = self.perform_destroy(instance)
        http_code = data.pop("code", None)
        return Response(data=data, status=http_code)

class ProductDestroyView(DestroyAPIView):
    """
    Product Delete API View
    """
    queryset = Product.objects.order_by("id").all()
    serializer_class = ProductListSerializer
    lookup_field = "object_id"

    def perform_destroy(self, instance):
        data = {}
        try:
            object_id = self.kwargs.get("object_id")
            policy_obj = Product.objects.get(object_id=object_id)

            policy_obj.delete()
            data["status"] = True
            data["message"] = "deleted"
            data["code"] = 200

        except Exception as exception:
            logger.exception("Exception occuring while fetching Request %s", exception)
            data["message"] = "something_went_wrong"
            data["status"] = "failed"
            data["code"] = 500
        return data

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        data = self.perform_destroy(instance)
        http_code = data.pop("code", None)
        return Response(data=data, status=http_code)