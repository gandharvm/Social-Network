from django.shortcuts import render, render_to_response,HttpResponse
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.urls import reverse, resolve
from mainapp.models import User
from mainapp.utils import *

modelList=[]

# view models list
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
    return render(mainRequest,"mainapp/models_List.html",context=context)

# display Main Menu
def displayMainMenu(request):
    # check if user is authenticated 
    # if not request.user.is_authenticated:
    #     return HttpResponseRedirect(reverse('loginPage'))
    modelList.append(menuItem("Send friend request",0))
    modelList.append(menuItem("Send private message",1))
    modelList.append(menuItem("Add post",2))
    modelList.append(menuItem("Add post",3))
    attr={'list':modelList,'title':'What to do next?','submitText':'Go!','responseType':'multi','returnFunction':"getMenuResponse" }
    return display_Menu(attr,request)

def getIndexList(string):
    k=[]
    for i in range(1,len(string)-1,2):
        k.append(int(string[i]))
    return(k)

# 
def getMenuResponse(request):
    # check if user is authenticated 
    # if not request.user.is_authenticated:
    #     return HttpResponseRedirect(reverse('loginPage'))
    
    responseType = request.POST['responseType']
    indexList = []
    if (responseType=='single') :        
        indexList = getIndexList(request.POST['indexList'])    
    elif(responseType=='multi') :
        indexList = request.POST.getlist('indexList')

    responseList=[]
    for index in indexList:
        responseList.append(modelList[int(index)])
    
    print(str(responseList))
    # TODO currently to test code
    return HttpResponse(responseList)
    