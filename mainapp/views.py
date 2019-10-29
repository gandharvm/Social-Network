from django.shortcuts import render, render_to_response,HttpResponse
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.urls import reverse, resolve
from mainapp.models import *
from mainapp.utils import *

modelList=[]
u=CommercialUser.objects.get(username="Gandharv")

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
    

def mainPage(request):
    timeline = Timeline.objects.get(timeline_of=u)
    postList=[str(post) for post in timeline.posts.all()]
    l=Private_Message.objects.filter(to_user=u)
    messageList=[str(e) for e in l]
    h=""
    if(isinstance(u,CommercialUser)):
        h="Commercial"
    elif(isinstance(u,PremiumUser)):
        h="Premium ("+str(u.plan)+")"
    elif(isinstance(u,CasualUser)):
        h="Casual"        
    attr={'name':u.username,'postList':postList,'messageList':messageList,'balance':u.wallet_money,
        'maxt':u.max_transactions,'transactions':u.transactions,'DOB':u.date_of_birth,'email':u.email_id,'aType':h}
    return render(request,"mainapp/mainPage.html",attr)

def getUpgradeResponse(request):
    button=request.POST['submit']
    global u
    if(button=="Go_Back"):
        return HttpResponseRedirect(reverse("mainPage"))
    elif(button=="Upgrade"):
        rList=getResponseList(request)
        l=0
        resp=rList[0]
        if(resp.index==1):
            l=u.toPremium('silver')
        if(resp.index==2):
            l=u.toPremium('gold')
        if(resp.index==3):
            l=u.toPremium('platinum')
        u=l
        print(u)
        return HttpResponseRedirect(reverse("mainPage"))


def upgradeAccount(request):
    global u
    timeline = Timeline.objects.get(timeline_of=u)
    postList=[str(post) for post in timeline.posts.all()]
    l=Private_Message.objects.filter(to_user=u)
    messageList=[str(e) for e in l]
    h=""
    if(isinstance(u,CommercialUser)):
        h="Commercial"
    elif(isinstance(u,PremiumUser)):
        h="Premium ("+str(u.plan)+")"
    elif(isinstance(u,CasualUser)):
        h="Casual"  
    attr={'name':u.username,'postList':postList,'messageList':messageList,'balance':u.wallet_money,'aType':h,
        'maxt':u.max_transactions,'transactions':u.transactions,'DOB':u.date_of_birth,'email':u.email_id,'msg':"You cannot upgrade!",}
    if(isinstance(u,CommercialUser)):
        return render(request,"mainapp/mainPage.html",attr)
    if(isinstance(u,PremiumUser)):
        return render(request,"mainapp/mainPage.html",attr)
    if(isinstance(u,CasualUser)):
        buttonlist=["Upgrade","Go_Back"]
        l=[menuItem("Silver (INR 50 PM)",1),menuItem("Gold (INR 100 PM)",2),menuItem("Platinum (INR 100 PM)",3)]
        attr={'list':l,'title':'Select your plan','buttonlist':buttonlist,'returnFunction':'getUpgradeResponse','responseType':'single'}
        return display_Menu(attr,request)

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
        print('ok')
        l=menuListCommercial
    buttonlist = ['GO']
    attr={'list':l,'title':'Welcome '+u.username,'responseType':'single','returnFunction':"getMenuResponse", 'buttonlist':buttonlist }
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
    attr={'list':l,'title':'Select requests to accept/decline','buttonlist':buttonlist,'responseType':'multi','returnFunction':"getFRADResponse"}
    return display_Menu(attr,request)

def moneyRequests(request):
    l=u.money_requests.all()
    buttonlist=["Accept","Decline","Go_Back"]
    attr={'list':l,'title':'Select requests to accept/decline','buttonlist':buttonlist,'responseType':'multi','returnFunction':"getMRADResponse"}
    return display_Menu(attr,request)

def viewFriends(request):
    l=u.friends.all()
    buttonlist=["View_Profile/Timeline","Unfriend","Send_Money_Request","Go_Back"]
    attr={'list':l,'title':'Here are your friends','buttonlist':buttonlist,'responseType':'single','returnFunction':"getFLResponse"}    
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
    m2=u.friends.all()
    l2=[]
    for element in l:
        if element not in m2 and element.pk!=u.pk:
            l2.append(element)
    buttonlist=['Send_request',"Go_back"]
    attr={'list':l2,'title':'Select persons to send friend request','buttonlist':buttonlist,'responseType':'multi','returnFunction':"getFriendRequestResponse" }
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

# TODO in view friends
def post_OnOthersTimeline(request):
    global u
    l=u.friends.all()
    attr = {'list':l,'title':'Post on friends Timeline','submitText':'Select','responseType':'single','returnFunction':"getPostOnOtherTimelineResponse1" }
    return display_Menu(attr,request)

def send_private_message(request):
    global u
    l=[]
    if(isinstance(u,CommercialUser)):
        l=CasualUser.objects.all()
    elif(isinstance(u,PremiumUser)):
        l=u.friends.all()
    buttonlist=["Select","Go_Back"]
    attr = {'list':l,'title':'Select a person to send message','buttonlist':buttonlist,'responseType':'single','returnFunction':"getSendPrivateMessageRequest1" }
    return display_Menu(attr,request)

def getResponseList(request):
    responseType = request.POST['responseType']

    indexList = []
    if('indexList' in request.POST.keys()):
        if (responseType=='single') :        
            indexList = getIndexList(request.POST['indexList'])    
        elif(responseType=='multi') :
            indexList = getIndexList_Mutli(request.POST.getlist('indexList')) 

        responseList=[]
        for index in indexList:
            responseList.append(modelList[int(index)])
        return(responseList)
    
    else:
        return(indexList)

def getFriendRequestResponse(request):
    buttonlist=['Send_request',"Go_back"]
    responseList=getResponseList(request)
    button= request.POST['submit']
    if(button=='Send_request'):
        for fr in responseList:
            u.send_friend_request(fr.pk)
        return HttpResponseRedirect(reverse('mainPage'))
    elif(button=="Go_back"):
        return HttpResponseRedirect(reverse('mainPage'))
    

def getMoneyRequestResponse1(request,responseList):
    l=intHolder.objects.get(pk=1)
    l.num=responseList[0].pk
    l.save()
    return enterMoneytoSend(request)

def getMoneyRequestResponse2(request):
    amount=request.POST['text']
    l=intHolder.objects.get(pk=1)
    u.send_money(float(amount),l.num)
    return displayMainMenu(request)

def getMRADResponse(request):
    responseList=getResponseList(request)
    button=request.POST['submit']
    if(button == "Accept"):
        for mrequest in responseList:
            u.accept_money(mrequest.pk)
        return displayMainMenu(request)
    elif(button=="Decline"):
        for mrequest in responseList:
            u.reject_money(mrequest.pk)
        return displayMainMenu(request)
    elif(button=="Go_Back"):
        return displayMainMenu(request)


def getFRADResponse(request):
    responseList=getResponseList(request)
    button= request.POST['submit']
    if(button == "Accept"):
        for frequest in responseList:
            u.accept_friend_request(frequest.pk)
        return HttpResponseRedirect(reverse('mainPage'))
    elif(button=="Decline"):
        for frequest in responseList:
            u.reject_friend_request(frequest.pk)
        return HttpResponseRedirect(reverse('mainPage'))
    elif(button=="Go_Back"):
        return HttpResponseRedirect(reverse('mainPage'))

def viewFriendProfile(friend,request):
    infoList=[]
    k=intHolder.objects.get(pk=1)
    k.num=friend.pk
    k.save()
    timeline = Timeline.objects.get(timeline_of=friend)
    postList=[str(post) for post in timeline.posts.all()]
    enablePost = friend.others_can_post
    if(friend.others_can_see_dob==True):
        infoList.append("DOB:- "+str(friend.date_of_birth))
    if(friend.others_can_see_email==True):
        infoList.append("E-mail:- "+str(friend.email_id))
    attr={'name':friend.username,'enablePost':enablePost,'infoList':infoList,'postList':postList}
    return(render(request,"mainapp/userProfile.html",attr))
        

def getFLResponse(request):
    responseList=getResponseList(request)
    button= request.POST['submit']
    if(button=="View_Profile/Timeline"):
        return viewFriendProfile(responseList[0],request)
    elif(button=="Unfriend"):
        u.unfriend(responseList[0].pk)
        return HttpResponseRedirect(reverse("mainPage"))
    elif(button=="Send_Money_Request"):
        return getMoneyRequestResponse1(request,responseList)
    elif(button=="Post_on_timeline"):
        pass
    elif(button=="Go_Back"):
        return HttpResponseRedirect(reverse("mainPage"))
    

def getAccept_MoneyRequestResponse(request):
    responseList=getResponseList(request)
    u.accept_money(responseList[0].pk)
    return HttpResponseRedirect(reverse('displayMainMenu'))

def getDecline_MoneyRequestResponse(request):
    responseList=getResponseList(request)
    u.reject_money(responseList[0].pk)
    return HttpResponseRedirect(reverse('displayMainMenu'))

def getPostOnOwnTimelineResponse(request):
    text = request.POST['potText']
    text = text[:500]
    u.post_on_own_timeline(text)
    return HttpResponseRedirect(reverse('mainPage'))

def getPostOnOtherTimelineResponse1(request):
    responseList=getResponseList(request)
    l=intHolder.objects.get(pk=1)
    l.num=responseList[0].pk
    l.save()
    attr={'title':"Enter Post Content",'submitText':"Post",'returnFunction':'getPostOnOtherTimelineResponse2'}
    return display_textbox(attr,request)

def getPostOnOtherTimelineResponse2(request):
    text = request.POST['potText']
    text = text[:500]
    l=intHolder.objects.get(pk=1)
    u.post_on_other_timeline(l.num,text)
    return viewFriendProfile(CasualUser.objects.get(pk=l.num),request)    

def getSendPrivateMessageRequest1(request):
    buttonlist=["Select","Go_Back"]
    button=request.POST['submit']
    if(button==buttonlist[0]):
        responseList=getResponseList(request)
        l=intHolder.objects.get(pk=1)
        l.num=responseList[0].pk
        l.save()
        attr={'title':"Enter Messsage",'submitText':"Send",'returnFunction':'getSendPrivateMessageRequest2'}
        return display_textbox(attr,request)
    else:
        return HttpResponseRedirect(reverse('mainPage'))    


def getSendPrivateMessageRequest2(request):
    text = request.POST['text']
    text = text[:500]
    l=intHolder.objects.get(pk=1)
    u.send_message(l.num,text)
    return HttpResponseRedirect(reverse('mainPage'))   

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
    if(response.index==-2):
        return viewFriends(request)
    if(response.index==-3):
        return moneyRequests(request)
    if(response.index==1):
        return sendFriendRequest(request)

# TODO Not in use    
    # if(response.index==2):
    #     return acceptFriendRequest(request)
    # if(response.index==3):
    #     return declineFriendRequest(request)
    # if(response.index==4):
    #     return unfriend(request)

    if(response.index==5):
        return depositMoney(request)

# TODO Not in use
    # if(response.index==6):
    #     return sendMoneyRequest(request)

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
    if(response.index==14):
        return privacySettings(request)
    if(response.index==17):
        return send_private_message(request)

    return HttpResponse(responseList)

def getPageResponse(request):
    content=request.POST['text']
    fk=Page.objects.filter(admin=u)
    if(fk.exists()):
        fk[0].content=content
        fk[0].save()
        print("+++++++++++++++++++++++++++++++++++")

    else:
        print("*************************************")
        u.create_page(content)
    return HttpResponseRedirect(reverse("mainPage"))

def createPage(request):
    attr={'title':"Enter content for the page",'submitText':"Create Page",'returnFunction':"getPageResponse"}
    return display_textbox(attr,request)

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
    return HttpResponseRedirect(reverse('mainPage'))

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

def privacySettings(request):
    buttonList=["Confirm_Settings","Go_Back"]
    l=privacyList
    attr={'title':"Change your privacy settings here",'buttonlist':buttonList,'list':l,'responseType':'multi','returnFunction':"getPrivacyResponse"}
    return display_Menu(attr,request)

def getPrivacyResponse(request):
    button=request.POST['submit']
    responseList=getResponseList(request)
    if(button=="Go_Back"):
        return HttpResponseRedirect(reverse("mainPage"))
    elif(button=="Confirm_Settings"):
        u.others_can_post=False
        u.others_can_see_friends=False
        u.others_can_see_email=False
        u.others_can_see_dob=False
        for r in responseList:
            print(str(r))
            if(r.index==1):
                u.others_can_post=True
            elif(r.index==2):
                u.others_can_see_friends=True
            elif(r.index==3):
                u.others_can_see_email=True
            elif(r.index==4):
                u.others_can_see_dob=True
        print(u.others_can_post)
        u.save()
        return HttpResponseRedirect(reverse("mainPage"))



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

def viewPages(request):
    l=Page.objects.all()
    buttonlist=["View","Go_back"]
    attr={'title':"Select a page to view",'buttonlist':buttonlist,'list':l,'responseType':'single','returnFunction':"getVPResponse"}
    return display_Menu(attr,request)

def getVPResponse(request):
    button=request.POST['submit']
    if(button=="Go_back"):
        return HttpResponseRedirect(reverse("mainPage"))
    elif(button=="View"):
        rList=getResponseList(request)
        r=rList[0]
        print(r)
        attr={'username':r.admin,'content':r.Content}
        return render(request,"mainapp/page.html",attr)

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

def textForm_Multi(attr,request):
    return render(request,"mainapp/textForm_multiple.html",attr)


def createGroup(request):
    keys = ['Enter Group Name','Enter Maximum Number of members']
    buttonlist = ['create_group']
    attr= {
        'keys':keys,
        'title':'Create Group',
        'returnFunction':'getcreateGroupResponse',
        'buttonlist':buttonlist,
    }
    return textForm_Multi(attr,request)

def getcreateGroupResponse(request):
    # grp_Admin = GroupAdmin.objects.filter(user=u)
    # if (grp_Admin.exists()):
    #     grp_Admin[0].create_group()
    pass
