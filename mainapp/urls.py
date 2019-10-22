from django.urls import path, include
from mainapp import views

urlpatterns = [
    path("displayMainMenu/",views.displayMainMenu,name="displayMainMenu"),
    path("getMenuResponse/",views.getMenuResponse,name="getMenuResponse"),
]