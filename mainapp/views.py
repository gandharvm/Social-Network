from django.shortcuts import render, render_to_response,HttpResponse
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.urls import reverse, resolve
from mainapp.models import *
from mainapp.utils import *

modelList=[]
u=CasualUser.objects.get(username="Udayaan")
# u=CasualUser()


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
    global u
    l=CasualUser.objects.all()
    m=u.pot_friends.all()
    m2=u.friends.all()
    l2=[]
    for element in l:
        if element not in m and element not in m2 and element!=u:
            l2.append(element)
    attr={'list':l2,'title':'Select a person to send friend request','submitText':'Send request','responseType':'single','returnFunction':"getFriendRequestResponse" }
    return display_Menu(attr,request)

def sendMoneyRequest(request):
    global u
    l=u.friends.all()
    attr={'list':l,'title':'Select a person to send money request','submitText':'Send request','responseType':'single','returnFunction':"getMoneyRequestResponse1" }
    return display_Menu(attr,request)

def acceptFriendRequest(request):
    global u
    l=u.friend_requests.all()
    attr={'list':l,'title':'Select a friend request to accept','submitText':'accept request','responseType':'single','returnFunction':"getFRAResponse" }
    return display_Menu(attr,request)

def declineFriendRequest(request):
    global u
    l=u.friend_requests.all()
    attr={'list':l,'title':'Select a friend request to decline','submitText':'decline request','responseType':'single','returnFunction':"getFRDResponse" }
    return display_Menu(attr,request)

def unfriend(request):
    global u
    l=u.friends.all()
    attr={'list':l,'title':'Select a friend to unfriend','submitText':'unfriend','responseType':'single','returnFunction':"getUnfriendResponse" }
    return display_Menu(attr,request)

def acceptMoneyRequest(request):
    global u
    l = u.money_requests.all()
    attr = {'list':l,'title':'Accept money from a friend','submitText':'accept','responseType':'single','returnFunction':"getAccept_MoneyRequestResponse" }
    return display_Menu(attr,request)

def declineMoneyRequest(request):
    global u
    l = u.money_requests.all()
    attr = {'list':l,'title':'Accept money from a friend','submitText':'accept','responseType':'single','returnFunction':"getDecline_MoneyRequestResponse" }
    return display_Menu(attr,request)

def post_OnOwnTimeline(request) :
    global u
    attr = {'title':"Type content on your Post",'submitText':"Post",'returnFunction':"getPostOnOwnTimelineResponse"}
    return display_textbox(attr,request)

def post_OnOthersTimeline(request):
    global u
    l=u.friends.all()
    attr = {'list':l,'title':'Post on friends Timeline','submitText':'Select','responseType':'single','returnFunction':"getPostOnOtherTimelineResponse1" }
    return display_Menu(attr,request)


def getResponseList(request):
    responseType = request.POST['responseType']
    indexList = []
    if (responseType=='single') :        
        indexList = getIndexList(request.POST['indexList'])    
    elif(responseType=='multi') :
        indexList = request.POST.getlist('indexList')

    responseList=[]
    for index in indexList:
        responseList.append(modelList[int(index)])
    return(responseList)

def getFriendRequestResponse(request):
    responseList=getResponseList(request)
    u.send_friend_request(responseList[0].pk)
    return displayMainMenu(request)


def getMoneyRequestResponse1(request):
    responseList=getResponseList(request)
    l=intHolder.objects.get(pk=1)
    l.num=responseList[0].pk
    l.save()
    return enterMoneytoSend(request)

def getMoneyRequestResponse2(request):
    amount=request.POST['text']
    l=intHolder.objects.get(pk=1)
    u.send_money(float(amount),l.num)
    return displayMainMenu(request)

def getFRAResponse(request):
    responseList=getResponseList(request)
    u.accept_friend_request(responseList[0].pk)
    return displayMainMenu(request)

def getFRDResponse(request):
    responseList=getResponseList(request)
    u.reject_friend_request(responseList[0].pk)
    return displayMainMenu(request)

def getUnfriendResponse(request):
    responseList=getResponseList(request)
    u.unfriend(responseList[0].pk)
    return displayMainMenu(request)

def getAccept_MoneyRequestResponse(request):
    responseList=getResponseList(request)
    u.accept_money(responseList[0].pk)
    return HttpResponseRedirect(reverse('displayMainMenu'))

def getDecline_MoneyRequestResponse(request):
    responseList=getResponseList(request)
    u.reject_money(responseList[0].pk)
    return HttpResponseRedirect(reverse('displayMainMenu'))

def getPostOnOwnTimelineResponse(request):
    text = request.POST['text']
    text = text[:500]
    u.post_on_own_timeline(text)
    return HttpResponseRedirect(reverse('displayMainMenu'))

def getPostOnOtherTimelineResponse1(request):
    responseList=getResponseList(request)
    l=intHolder.objects.get(pk=1)
    l.num=responseList[0].pk
    l.save()
    attr={'title':"Enter Post Content",'submitText':"Post",'returnFunction':'getPostOnOtherTimelineResponse2'}
    return display_textbox(attr,request)

def getPostOnOtherTimelineResponse2(request):
    text = request.POST['text']
    text = text[:500]
    l=intHolder.objects.get(pk=1)
    u.post_on_other_timeline(l.num,text)
    return HttpResponseRedirect(reverse('displayMainMenu'))    

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
    
    #TODO
    response=responseList[0]
    if(response.index==1):
        return sendFriendRequest(request)
    if(response.index==2):
        return acceptFriendRequest(request)
    if(response.index==3):
        return declineFriendRequest(request)
    if(response.index==4):
        return unfriend(request)
    if(response.index==5):
        return depositMoney(request)
    if(response.index==6):
        return sendMoneyRequest(request)
    if(response.index==7):
        return acceptMoneyRequest(request)
    if(response.index==8):
        return declineMoneyRequest(request)
    if(response.index==9):
        return post_OnOwnTimeline(request)
    if(response.index==10):
        return post_OnOthersTimeline(request)

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

def depositMoney(request):
    attr={'title':"Enter amount to deposit",'submitText':"Deposit",'returnFunction':'getDepositResponse'}
    return display_textbox(attr,request)

def enterMoneytoSend(request):
    attr={'title':"Enter amount to send",'submitText':"Send",'returnFunction':'getMoneyRequestResponse2'}
    return display_textbox(attr,request)

def getDepositResponse(request):
    amount=request.POST['text']
    u.deposit_money(float(amount))
    return displayMainMenu(request)

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