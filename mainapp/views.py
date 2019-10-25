from django.shortcuts import render, render_to_response,HttpResponse
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.urls import reverse, resolve
from mainapp.models import *
from mainapp.utils import *

modelList=[]
u=PremiumUser()

# view models list
def display_Menu(request,mainRequest) :
    # check if user is authenticated 
    # if not request.user.is_authenticated:
    #     return HttpResponseRedirect(reverse('loginPage'))
    global modelList
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
    l=[]
    if(isinstance(u,CasualUser)):
        l=menuListCasual
    if(isinstance(u,PremiumUser)):
        l=menuListPremium
    if(isinstance(u,CommercialUser)):
        l=menuListCommercial
    attr={'list':l,'title':'What to do next?','submitText':'Go!','responseType':'single','returnFunction':"getMenuResponse" }
    return display_Menu(attr,request)

def getIndexList(string):
    k=[]
    for i in range(1,len(string)-1,2):
        k.append(int(string[i]))
    return(k)

def sendFriendRequest(request):
    l=CasualUser.objects.all()
    attr={'list':l,'title':'Select a person to send friend request','submitText':'Send request','responseType':'single','returnFunction':"getFriendRequestResponse" }
    return display_Menu(attr,request)

def getFriendRequestResponse(request):
    responseType = request.POST['responseType']
    print(modelList)
    indexList = []
    if (responseType=='single') :        
        indexList = getIndexList(request.POST['indexList'])    
    elif(responseType=='multi') :
        indexList = request.POST.getlist('indexList')

    responseList=[]
    for index in indexList:
        responseList.append(modelList[int(index)])

    u.send_friend_request(responseList[0].pk)
    return HttpResponse(responseList)   


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
    
    # print(str(responseList))
    # # TODO currently to test code

    response=responseList[0]
    if(response.index==1):
        return sendFriendRequest(request)

    return HttpResponse(responseList)
    