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
    responseType=attr['responseType']
    returnFunction=attr['returnFunction']
    buttonlist=attr['buttonlist']
    displayList = []
    for model in modelList :
        displayList.append(str(model))
    context = {
        "buttonlist" : buttonlist,
        "displayList" : displayList,
        "rangeList": range(len(displayList)),
        "title": title,
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
    buttonlist = ['GO']
    attr={'list':l,'title':'What to do next?','responseType':'single','returnFunction':"getMenuResponse", 'buttonlist':buttonlist }
    return display_Menu(attr,request)

# parsing string list for single responsetype
def getIndexList(string):
    k=[]
    string = string[1:len(string)-1]
    string = string.split(',')
    for i in range(0,len(string)-1):
        k.append(int(string[i]))
    return(k)

def friendRequests(request):
    l=u.friend_requests.all()
    buttonlist=["Accept","Decline","Go_Back"]
    attr={'list':l,'title':'Select a request to accept/decline','buttonlist':buttonlist,'responseType':'single','returnFunction':"getFRADResponse"}
    return display_Menu(attr,request)


# parsing string list for multiple responsetype
def getIndexList_Mutli(stringList):
    k=[]
    for i in stringList :
        index = getIndexList(i)
        k.append(index[0])
    return k

def sendFriendRequest(request):
    global u
    l=CasualUser.objects.all()
    m=u.pot_friends.all()
    m2=u.friends.all()
    l2=[]
    for element in l:
        if element not in m and element not in m2 and element!=u:
            l2.append(element)
    buttonlist=['Send request']
    attr={'list':l2,'title':'Select a person to send friend request','buttonlist':buttonlist,'responseType':'single','returnFunction':"getFriendRequestResponse" }
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

def send_private_message(request):
    global u
    l=u.friends.all()
    attr = {'list':l,'title':'Select friend to send message','submitText':'Select','responseType':'single','returnFunction':"getSendPrivateMessageRequest1" }
    return display_Menu(attr,request)

def getResponseList(request):
    responseType = request.POST['responseType']

    indexList = []
    if('indexList' in request.POST.keys()):
        if (responseType=='single') :        
            indexList = getIndexList(request.POST['indexList'])    
        elif(responseType=='multi') :
            indexList = request.POST.getlist('indexList')

        responseList=[]
        for index in indexList:
            responseList.append(modelList[int(index)])
        return(responseList)
    
    else:
        return(indexList)

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

def getFRADResponse(request):
    responseList=getResponseList(request)
    button= request.POST['submit']
    if(button == "Accept"):
        u.accept_friend_request(responseList[0].pk)
        return displayMainMenu(request)
    elif(button=="Decline"):
        u.reject_friend_request(responseList[0].pk)
        return displayMainMenu(request)
    elif(button=="Go_Back"):
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

def getSendPrivateMessageRequest1(request):
    responseList=getResponseList(request)
    l=intHolder.objects.get(pk=1)
    l.num=responseList[0].pk
    l.save()
    attr={'title':"Enter Messsage",'submitText':"Send",'returnFunction':'getSendPrivateMessageRequest2'}
    return display_textbox(attr,request)

def getSendPrivateMessageRequest2(request):
    text = request.POST['text']
    text = text[:500]
    l=intHolder.objects.get(pk=1)
    u.send_message(l.num,text)
    return HttpResponseRedirect(reverse('displayMainMenu'))   

def getMenuResponse(request):
    # check if user is authenticated 
    # if not request.user.is_authenticated:
    #     return HttpResponseRedirect(reverse('loginPage'))
    
    responseType = request.POST['responseType']
    button= request.POST['submit']
    indexList = []
    if (responseType=='single') :        
        indexList = getIndexList(request.POST['indexList'])    
    elif(responseType=='multi') :
        indexList = getIndexList_Mutli(request.POST.getlist('indexList')) 

    print(indexList,"---------------------------")
    responseList=[]
    for index in indexList:
        responseList.append(modelList[int(index)])
    
    #TODO
    response=responseList[0]
    if(response.index==-1):
        return friendRequests(request)
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
    if(response.index==11):
        return viewMyPosts(request)
    if(response.index==12):
        return viewFriendsPost(request)
    if(response.index==17):
        return send_private_message(request)

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

def viewContentlist(attr,request):
    # check if user is authenticated 
    # if not request.user.is_authenticated:
    #     return HttpResponseRedirect(reverse('loginPage'))
    title=attr['title']
    modelList=attr['list']
    contentList=[]
    for model in modelList :
        contentList.append(str(model))
    print(contentList,"-----------------------------------")
    context = {
        "contentList" : contentList,
        "title": title,
    }
    return render(request,"mainapp/contentList.html",context=context)

def viewMyPosts(request):
    global u
    mytimeline=Timeline.objects.get(timeline_of=u)
    posts=mytimeline.posts.all()
    attr = {
        "list":posts,
        "title":"Posts on your timline",
    }
    return viewContentlist(attr,request)

def viewFriendsPost(request):
    global u
    l=u.friends.all()
    attr = {'list':l,'title':'Select friend','submitText':'Select','responseType':'single','returnFunction':"getViewPostOfFriendResponse" }
    return display_Menu(attr,request)

def getViewPostOfFriendResponse(request):
    responseList=getResponseList(request)
    friend = responseList[0]
    timeline = Timeline.objects.get(timeline_of=friend)
    posts=timeline.posts.all()
    attr = {
        "list":posts,
        "title":"Posts on "+ friend.username +" timline",
    }
    return viewContentlist(attr,request)