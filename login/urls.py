from django.urls import path, include
from login import views

urlpatterns = [
    path('',views.loginPage,name='loginPage'),
    path('signUp/',views.signUpForm,name='signUpForm'),
    path('auth/',views.authentication,name='auth'),
    path('createUser/',views.createUser,name='createUser'),
    path('logout/',views.logout_view,name='logout'),
    
]