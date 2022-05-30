# OrderManagementSystem

How to use:
python manage.py runserver

URLs to target:

    #register user api
    http://127.0.0.1:8000/addUser/
    parameters: in Body as form data pass values example given below Post request
      email:consumeruser@gmail.com
      first_name:consumer
      last_name:user
      username:consumeruser@gmail.com
      password:passme123
      user_type:consumer
    #login api
    http://127.0.0.1:8000/login/
    parameters:Post request
    user_id:consumeruser@gmail.com
    password:passme123
    http://127.0.0.1:8000/logout/
    #api to add product
    http://127.0.0.1:8000/addproduct/
    post request
    product_name:cheetos
    product_description:cheetos
    #api to edit a product
    http://127.0.0.1:8000/http://127.0.0.1:8000/editproduct/<str:object_id>
    Put request
    product_name:cheetos
    product_description:cheetos
    #list all the products
    http://127.0.0.1:8000/product/list/
    get request
    #api for deleting a product
    http://127.0.0.1:8000/product-delete/<str:object_id>/
    #api to create a order
    
    http://127.0.0.1:8000/addorder/
    Post request
    parameters should be passed in body
    product_id:4
    user_id:5
    #api for editing a order
    http://127.0.0.1:8000/editorder/<str:object_id>
    PUT request
    parameters should be passed in body
    product_id:4
    user_id:5
    #api for listing all orders
    http://127.0.0.1:8000/order/list/
    #api for deleting a order
    http://127.0.0.1:8000/order-delete/<str:object_id>/
    
    
    
    to get object_id we can just run list apis 
    superadmin username: admin
    superadmin password: admin123
    
    
    Useful commands:
python manage.py createsuperuser
python manage.py makemigrations
python manage.py migrate
  
