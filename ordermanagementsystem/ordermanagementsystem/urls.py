"""ordermanagementsystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from oms import views
from oms.views import Record,Login,Logout,ProductCreateView,ProductListView,ProducteditView,OrderCreateView,OrdereditView,OrderListView
from rest_framework import routers




router = routers.DefaultRouter()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    #register user api
    path('addUser/', Record.as_view(), name="register"),
    #login api
    path('login/', Login.as_view(), name="login"),
    path('logout/', Logout.as_view(), name="logout"),
    #api to add product
    path('addproduct/', ProductCreateView.as_view(), name="product_create"),
    #api to edit a product
    path('editproduct/<str:object_id>', ProducteditView.as_view(), name="product_edit"),
    #list all the products
    path('product/list/', ProductListView.as_view(), name="product_list"),
    #api for deleting a product
    path("product-delete/<str:object_id>/",views.ProductDestroyView.as_view(),name="product-delete-api"),\
    #api to create a order
    path('addorder/', OrderCreateView.as_view(), name="order_create"),
    #api for editing a order
    path('editorder/<str:object_id>', OrdereditView.as_view(), name="order_edit"),
    #api for listing all orders
    path('order/list/', OrderListView.as_view(), name="order_list"),
    #api for deleting a order
    path("order-delete/<str:object_id>/",views.OrderDestroyView.as_view(),name="order-delete-api"),

]
