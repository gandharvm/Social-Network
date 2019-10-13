from django.urls import path, include
from mainapp import views

urlpatterns = [
    path("user_List/",views.user_List,name="user_List"),
    path("getUser/",views.getUser,name="getUser"),
]