from django.shortcuts import render, render_to_response, HttpResponse
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, resolve
from mainapp.models import CasualUser

# view users list


def user_List(request):
    # check if user is authenticated
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('loginPage'))
    users = CasualUser.objects.all()
    Names_List = []
    for user in users:
        Names_List.append(user.username)
    context = {
        "usersList": Names_List,
    }
    return render(request, "mainapp/user_List.html", context=context)

# view user profile


def getUser(request):
    # check if user is authenticated
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('loginPage'))
    username = request.POST['username']
    return HttpResponse(username)
