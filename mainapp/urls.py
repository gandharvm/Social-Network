from django.urls import path, include
from mainapp import views

urlpatterns = [
    path("displayMainMenu/",views.displayMainMenu,name="displayMainMenu"),
    path("getMenuResponse/",views.getMenuResponse,name="getMenuResponse"),
    path("getFriendRequestResponse/",views.getFriendRequestResponse,name="getFriendRequestResponse"),
    path("getMoneyRequestResponse1/",views.getMoneyRequestResponse1,name="getMoneyRequestResponse1"),
    path("getMoneyRequestResponse2/",views.getMoneyRequestResponse2,name="getMoneyRequestResponse2"),
    path("getPrivacyResponse/",views.getPrivacyResponse,name="getPrivacyResponse"),
    path("getFRADResponse/",views.getFRADResponse,name="getFRADResponse"),
    path("getMRADResponse/",views.getMRADResponse,name="getMRADResponse"),
    path("getFLResponse/",views.getFLResponse,name="getFLResponse"),
    path("getDepositResponse/",views.getDepositResponse,name="getDepositResponse"),
    path("getAccept_MoneyRequestResponse/",views.getAccept_MoneyRequestResponse,name="getAccept_MoneyRequestResponse"),
    path("getPostOnOwnTimelineResponse/",views.getPostOnOwnTimelineResponse,name="getPostOnOwnTimelineResponse"),
    path("getPostOnOtherTimelineResponse1/",views.getPostOnOtherTimelineResponse1,name="getPostOnOtherTimelineResponse1"),
    path("getPostOnOtherTimelineResponse2/",views.getPostOnOtherTimelineResponse2,name="getPostOnOtherTimelineResponse2"),
    path("getSendPrivateMessageRequest1/",views.getSendPrivateMessageRequest1,name="getSendPrivateMessageRequest1"),
    path("getSendPrivateMessageRequest2/",views.getSendPrivateMessageRequest2,name="getSendPrivateMessageRequest2"),
    path("getViewPostOfFriendResponse",views.getViewPostOfFriendResponse,name="getViewPostOfFriendResponse"),
    path("privacySettings/",views.privacySettings,name="privacySettings"),
    path("mainPage/",views.mainPage,name="mainPage"),
    path("upgradeAccount/",views.upgradeAccount,name="upgradeAccount"),
    path("send_private_message/",views.send_private_message,name="send_private_message"),
    path("getUpgradeResponse/",views.getUpgradeResponse,name="getUpgradeResponse"),    
    path("depositMoney/",views.depositMoney,name="depositMoney"),
    path("viewFriends/",views.viewFriends,name="viewFriends"),
    path("viewFriendProfile/",views.viewFriendProfile,name="viewFriendProfile"),
    path("sendFriendRequest/",views.sendFriendRequest,name="sendFriendRequest"),
    path("friendRequests/",views.friendRequests,name="friendRequests"),
    path("createPage/",views.createPage,name="createPage"),
    path("getPageResponse/",views.getPageResponse,name="getPageResponse"),
    path("viewPages/",views.viewPages,name="viewPages"),
    path("getVPResponse/",views.getVPResponse,name="getVPResponse"),    
    path('createGroup',views.createGroup,name="createGroup"),
    path("getcreateGroupResponse",views.getcreateGroupResponse,name="getcreateGroupResponse"),
]