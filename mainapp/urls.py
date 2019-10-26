from django.urls import path, include
from mainapp import views

urlpatterns = [
    path("displayMainMenu/",views.displayMainMenu,name="displayMainMenu"),
    path("getMenuResponse/",views.getMenuResponse,name="getMenuResponse"),
    path("getFriendRequestResponse/",views.getFriendRequestResponse,name="getFriendRequestResponse"),
    path("getMoneyRequestResponse1/",views.getMoneyRequestResponse1,name="getMoneyRequestResponse1"),
    path("getMoneyRequestResponse2/",views.getMoneyRequestResponse2,name="getMoneyRequestResponse2"),
    path("getFRAResponse/",views.getFRAResponse,name="getFRAResponse"),
    path("getFRDResponse/",views.getFRDResponse,name="getFRDResponse"),
    path("getUnfriendResponse/",views.getFRDResponse,name="getUnfriendResponse"),
    path("getDepositResponse/",views.getDepositResponse,name="getDepositResponse"),
    path("getAccept_MoneyRequestResponse",views.getAccept_MoneyRequestResponse,name="getAccept_MoneyRequestResponse"),
    # below two urls for testing text box
    path("testTextBox/",views.testTextBox, name="testTextBox"),
    path("getTextResponse/",views.getTextResponse,name="getTextResponse"),
]