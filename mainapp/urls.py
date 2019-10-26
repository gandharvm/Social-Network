from django.urls import path, include
from mainapp import views

urlpatterns = [
    path("displayMainMenu/",views.displayMainMenu,name="displayMainMenu"),
    path("getMenuResponse/",views.getMenuResponse,name="getMenuResponse"),
    path("getFriendRequestResponse/",views.getFriendRequestResponse,name="getFriendRequestResponse"),
    # below two urls for testing text box
    path("testTextBox/",views.testTextBox, name="testTextBox"),
    path("getTextResponse/",views.getTextResponse,name="getTextResponse"),
]