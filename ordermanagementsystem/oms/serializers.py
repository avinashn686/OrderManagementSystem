from django.contrib.auth.models import User, Group

from rest_framework import serializers


from django.db.models import Q # for queries
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User,Product,Order
from django.core.exceptions import ValidationError
from uuid import uuid4


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
        )
    username = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
        )
    password = serializers.CharField(max_length=50)
    # User.objects.create()
    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'password',
            'first_name',
            'last_name',
            'user_type'
        )


class UserLoginSerializer(serializers.ModelSerializer):
    # to accept either username or email
    user_id = serializers.CharField()
    password = serializers.CharField()
    token = serializers.CharField(required=False, read_only=True)

    def validate(self, data):
        # user,email,password validator
        user_id = data.get("user_id", None)
        password = data.get("password", None)
        if not user_id and not password:
            raise ValidationError("Details not entered.")
        user = None
        # if the email has been passed
        if '@' in user_id:
            user = User.objects.filter(
                Q(email=user_id) &
                Q(password=password)
                ).distinct()
            if not user.exists():
                raise ValidationError("User credentials are not correct.")
            user = User.objects.get(email=user_id)
        else:
            user = User.objects.filter(
                Q(username=user_id) &
                Q(password=password)
            ).distinct()
            if not user.exists():
                raise ValidationError("User credentials are not correct.")
            user = User.objects.get(username=user_id)
        if user.ifLogged:
            raise ValidationError("User already logged in.")
        user.ifLogged = True
        data['token'] = uuid4()
        user.token = data['token']
        user.save()
        return data

    class Meta:
        model = User
        fields = (
            'user_id',
            'password',
            'token'

        )

        read_only_fields = (
            'token',
        )


class UserLogoutSerializer(serializers.ModelSerializer):
    token = serializers.CharField()
    status = serializers.CharField(required=False, read_only=True)

    def validate(self, data):
        token = data.get("token", None)
        print(token)
        user = None
        try:
            user = User.objects.get(token=token)
            if not user.ifLogged:
                raise ValidationError("User is not logged in.")
        except Exception as e:
            raise ValidationError(str(e))
        user.ifLogged = False
        user.token = ""
        user.save()
        data['status'] = "User is logged out."
        return data

    class Meta:
        model = User
        fields = (
            'token',
            'status',
        )
class ProductCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            'product_name',
            'product_description',

        ]
    def create(self, validated_data):
        project_obj = Product.objects.create(product_name=validated_data['product_name'],product_description=validated_data['product_description'])
        return project_obj
    def update(self, instance, validated_data):
        requests = self._kwargs["context"].get("request")
        request=requests.data
        fields = instance._meta.fields
        for field_name in fields:
            setattr(
                instance,
                field_name.name,
                request.get(field_name.name, getattr(instance, field_name.name)),
            )
        instance.save()
        return instance

class ProductListSerializer(serializers.ModelSerializer):
        class Meta:
            model = Product
            fields = '__all__'

class OrderCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'product_id',
            'user_id',

        ]
    def create(self, validated_data):
        project_obj = Order.objects.create(product_id=validated_data['product_id'],user_id=validated_data['user_id'])
        return project_obj
    def update(self, instance, validated_data):
        requests = self._kwargs["context"].get("request")
        request=requests.data
        fields = instance._meta.fields
        product=Product.objects.get(id = request.get('product_id'))
        user=User.objects.get(id = request.get('user_id'))
        instance.user_id=user
        instance.product_id=product
        instance.save()
        return instance

class OrderListSerializer(serializers.ModelSerializer):
        class Meta:
            model = Order
            fields = '__all__'
