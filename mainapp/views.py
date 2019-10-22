from django.shortcuts import render, render_to_response,HttpResponse
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.urls import reverse, resolve
from mainapp.models import User
from mainapp.utils import *

modelList=[]

# view users list
def display_Menu(request,mainRequest) :
    # check if user is authenticated 
    # if not request.user.is_authenticated:
    #     return HttpResponseRedirect(reverse('loginPage'))
    modelList=request['list']
    title=request['title']
    submitText=request['submitText']
    responseType=request['responseType']
    returnFunction=request['returnFunction']
    displayList = []
    for model in modelList :
        displayList.append(str(model))
    context = {
        "displayList" : displayList,
        "rangeList": range(len(displayList)),
        "title": title,
        "submitText": submitText,
        "returnFunction":returnFunction,
        "responseType":responseType
    }
    return render(mainRequest,"mainapp/user_List.html",context=context)


def displayMainMenu(request):
    items=[]
    items.append(menuItem("Send friend request",1))
    items.append(menuItem("Send private message",2))
    items.append(menuItem("Display friend list",3))
    items.append(menuItem("Add post",4))
    attr={'list':items,'title':'What to do next?','submitText':'Go!','responseType':'single','returnFunction':"getMenuResponse"}

    return display_Menu(attr,request)

# view user profile
def getMenuResponse(request) :
    # check if user is authenticated 
    # if not request.user.is_authenticated:
    #     return HttpResponseRedirect(reverse('loginPage'))
    indexList = request.POST['indexList']
    responseList=[]
    for index in indexList:
        responseList.append(modelList[index])
    print(responseList)
    # return HttpResponse(responseList)
    