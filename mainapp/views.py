from django.shortcuts import render, render_to_response,HttpResponse
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.urls import reverse, resolve
from mainapp.models import *
from mainapp.utils import *

modelList=[]
u=PremiumUser()

# view models list
def display_Menu(attr,request) :
    # check if user is authenticated 
    # if not request.user.is_authenticated:
    #     return HttpResponseRedirect(reverse('loginPage'))
    global modelList
    modelList=attr['list']
    title=attr['title']
    submitText=attr['submitText']
    responseType=attr['responseType']
    returnFunction=attr['returnFunction']
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
    return render(request,"mainapp/models_List.html",context=context)

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

# display text box
def display_textbox(attr,request) :
    # TODO user.is_authenticated = ?
    title=attr['title']
    submitText=attr['submitText']
    returnFunction=attr['returnFunction']
    context = {    
        "title": title,
        "submitText": submitText,
        "returnFunction":returnFunction,
    }
    return render(request,"mainapp/textform.html",context)

# receive text response
def getTextResponse(request):
    # TODO user.is_authenticated = ?
    text = request.POST['text']
    # TODO remove next line (just for testing)
    return HttpResponse(text)

# test text box
def testTextBox(request):
    # TODO user.is_authenticated = ?
    attr = {
        "title":"Title",
        "submitText": "submit",
        "returnFunction":"getTextResponse",
    }
    return display_textbox(attr,request)