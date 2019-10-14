from django.shortcuts import render, render_to_response,HttpResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, resolve
from mainapp.models import User

# Create your views here.

# view users list
def user_List(request) :
    users = User.objects.all()
    Names_List = []
    for user in users :
        Names_List.append(user.username)
    context = {
        "usersList" : Names_List,
    }
    return render(request,"mainapp/user_List.html",context=context)

# view user profile
def getUser(request) :
    username = request.POST['username']
    return HttpResponse(username)