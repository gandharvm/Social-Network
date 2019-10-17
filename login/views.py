from django.shortcuts import render, render_to_response,HttpResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, resolve
from mainapp.models import CasualUser, PremiumUser, CommercialUser, User
from django.contrib.auth import authenticate, login, logout, models, logout
import json

# show login Page
def loginPage(request) :
    return render(request,"login/loginPage.html")

# authentication
def authentication(request) :
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse('user_List'))
    else:
        return HttpResponseRedirect(reverse('loginPage'))

# logout 
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('loginPage'))

#  show sign up form
def signUpForm(request):
    users = User.objects.all()
    Names_List = []
    for user in users :
        Names_List.append(user.username)
    context = {
        "len" : len(Names_List),
        "names" : json.dumps(Names_List),
    }
    return render(request,"login/SignUpForm.html",context)

# create user     
def createUser(request):
    username = request.POST['username']
    password = request.POST['password']
    confirmPassword = request.POST['confirmPassword']
    email = request.POST['email']
    category = request.POST['category']
    newUser = models.User.objects.create_user(username, email, password)
    
    # Create user model instance 
    user = None
    if (category=="casual"):
        user = CasualUser(username=username,category=category)
    elif(category=="premium"):
        user = PremiumUser(username=username,category=category)
    elif(category=="commercial"):
        user = CommercialUser(username=username,category=category)
    user.save()

    # TODO add OTP verification of email
    return HttpResponseRedirect(reverse('loginPage'))