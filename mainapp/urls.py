from django.urls import path, include
from mainapp import views

urlpatterns = [
    path("displayMainMenu/",views.displayMainMenu,name="displayMainMenu"),
    path("getMenuResponse/",views.getMenuResponse,name="getMenuResponse"),
    path("getFriendRequestResponse/",views.getFriendRequestResponse,name="getFriendRequestResponse"),
    path("getMoneyRequestResponse1/",views.getMoneyRequestResponse1,name="getMoneyRequestResponse1"),
    path("getMoneyRequestResponse2/",views.getMoneyRequestResponse2,name="getMoneyRequestResponse2"),
    path("getPrivacyResponse/",views.getPrivacyResponse,name="getPrivacyResponse"),
    path("getFRAResponse/",views.getFRAResponse,name="getFRAResponse"),
    path("getFRADResponse/",views.getFRADResponse,name="getFRADResponse"),
    path("getFLResponse/",views.getFLResponse,name="getFLResponse"),
    path("getFRDResponse/",views.getFRDResponse,name="getFRDResponse"),
    path("getUnfriendResponse/",views.getFRDResponse,name="getUnfriendResponse"),
    path("getDepositResponse/",views.getDepositResponse,name="getDepositResponse"),
    path("getAccept_MoneyRequestResponse/",views.getAccept_MoneyRequestResponse,name="getAccept_MoneyRequestResponse"),
    path("getPostOnOwnTimelineResponse/",views.getPostOnOwnTimelineResponse,name="getPostOnOwnTimelineResponse"),
    path("getPostOnOtherTimelineResponse1/",views.getPostOnOtherTimelineResponse1,name="getPostOnOtherTimelineResponse1"),
    path("getPostOnOtherTimelineResponse2/",views.getPostOnOtherTimelineResponse2,name="getPostOnOtherTimelineResponse2"),
    path("getSendPrivateMessageRequest1/",views.getSendPrivateMessageRequest1,name="getSendPrivateMessageRequest1"),
    path("getSendPrivateMessageRequest2/",views.getSendPrivateMessageRequest2,name="getSendPrivateMessageRequest2"),
    path("getViewPostOfFriendResponse",views.getViewPostOfFriendResponse,name="getViewPostOfFriendResponse"),
]