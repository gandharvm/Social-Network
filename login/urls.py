from django.urls import path, include
from login import views

urlpatterns = [
    path('', views.loginPage, name='loginPage'),
    path('signUp/', views.signUpForm, name='signUpForm'),
    path('auth/', views.authentication, name='auth'),
    path('createUser/', views.createUser, name='createUser'),
    path('logout/', views.logout_view, name='logout'),
    path('signUp/otp/', views.otp_page, name='otp'),
    path('choosePlan/', views.choosePlan, name='plan'),
    path('forgotPass/', views.forgotPass, name='forgotPass'),
    path('forgotPass/sendOTP', views.sendOTP, name='sendOTP'),
    path('forgotPass/verify', views.changePass, name='verify'),

]
