from django.shortcuts import render, render_to_response,HttpResponse
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.urls import reverse, resolve
from mainapp.models import *
from mainapp.utils import *

from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from login.utils import TOTPVerification

# modelList=[]
# u=CommercialUser.objects.get(username="udayaan17119Commercial")
# u = None`
# u=CasualUser()
# otp_mail = TOTPVerification()

# error = ''

def retrieveUser(request):
    u1=CasualUser.objects.get(username=request.user.username)
    if(u1.category=='commercial'):
        u1=CommercialUser.objects.get(username=u1.username)
    elif(u1.category=='premium'):
        u1=PremiumUser.objects.get(username=u1.username)
    return u1

# view models list
def display_Menu(attr,request) :
    # check if user is authenticated 
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('loginPage'))
    u = retrieveUser(request)
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
        "responseType":responseType,
        "Error":u.error
    }
    u.error = ''
    u.save()
    return render(request,"mainapp/models_List.html",context=context)
    

def mainPage(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('loginPage'))

    u = retrieveUser(request)
    
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
        'maxt':u.max_transactions,'transactions':u.transactions,'DOB':u.date_of_birth,'email':u.email_id,'aType':h, 'Error': u.error}
    u.error = ''
    u.save()
    return render(request,"mainapp/mainPage.html",attr)

def getUpgradeResponse(request):
    # # check if user is authenticated 
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('loginPage'))
    
    button=request.POST['submit']
    u = retrieveUser(request)    
    if(button=="Go_Back"):
        return HttpResponseRedirect(reverse("mainPage"))
    elif(button=="Upgrade"):
        rList=getResponseList(request)
        l=0
        resp=rList[0]
        if(resp==0):
            l=u.toPremium('silver')
        if(resp==1):
            l=u.toPremium('gold')
        if(resp==2):
            l=u.toPremium('platinum')
        u=l
        return HttpResponseRedirect(reverse("mainPage"))


def upgradeAccount(request):
    
    # # check if user is authenticated 
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('loginPage'))
    u = retrieveUser(request)
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
        'maxt':u.max_transactions,'transactions':u.transactions,'DOB':u.date_of_birth,'email':u.email_id,'msg':"You cannot upgrade!",'Error':u.error}
    if(isinstance(u,CommercialUser)):
        u.error = ''
        u.save()
        return render(request,"mainapp/mainPage.html",attr)
    if(isinstance(u,PremiumUser)):
        u.error = ''
        u.save()
        return render(request,"mainapp/mainPage.html",attr)
    if(isinstance(u,CasualUser)):
        buttonlist=["Upgrade","Go_Back"]
        l=[menuItem("Silver (INR 50 PM)",1),menuItem("Gold (INR 100 PM)",2),menuItem("Platinum (INR 100 PM)",3)]
        attr={'list':l,'title':'Select your plan','buttonlist':buttonlist,'returnFunction':'getUpgradeResponse','responseType':'single'}
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
    # # check if user is authenticated 
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('loginPage'))
    u = retrieveUser(request)    
    l=u.friend_requests.all()
    buttonlist=["Accept","Decline","Go_Back"]
    attr={'list':l,'title':'Select requests to accept/decline','buttonlist':buttonlist,'responseType':'multi','returnFunction':"getFRADResponse"}
    return display_Menu(attr,request)

def moneyRequests(request):
    # # check if user is authenticated 
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('loginPage'))
    u = retrieveUser(request)    
    l=u.money_requests.all()
    buttonlist=["Accept","Decline","Go_Back"]
    attr={'list':l,'title':'Select requests to accept/decline','buttonlist':buttonlist,'responseType':'multi','returnFunction':"getMRADResponse"}
    return display_Menu(attr,request)

def viewFriends(request):
    # # check if user is authenticated 
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('loginPage'))
    u = retrieveUser(request)    
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
    # # check if user is authenticated 
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('loginPage'))
    u = retrieveUser(request)    
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
    # # check if user is authenticated 
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('loginPage'))
    u = retrieveUser(request)    
    l = u.money_requests.all()
    attr = {'list':l,'title':'Accept money from a friend','submitText':'accept','responseType':'single','returnFunction':"getAccept_MoneyRequestResponse" }
    return display_Menu(attr,request)

def declineMoneyRequest(request):
    # # check if user is authenticated 
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('loginPage'))
    u = retrieveUser(request)    
    l = u.money_requests.all()
    attr = {'list':l,'title':'Accept money from a friend','submitText':'accept','responseType':'single','returnFunction':"getDecline_MoneyRequestResponse" }
    return display_Menu(attr,request)

def post_OnOwnTimeline(request) :
    # # check if user is authenticated 
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('loginPage'))
    u = retrieveUser(request)    
    attr = {'title':"Type content on your Post",'submitText':"Post",'returnFunction':"getPostOnOwnTimelineResponse"}
    return display_textbox(attr,request)

# TODO in view friends
def post_OnOthersTimeline(request):
    # # check if user is authenticated 
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('loginPage'))
    u = retrieveUser(request)    
    l=u.friends.all()
    attr = {'list':l,'title':'Post on friends Timeline','submitText':'Select','responseType':'single','returnFunction':"getPostOnOtherTimelineResponse1" }
    return display_Menu(attr,request)

def send_private_message(request):
    # # check if user is authenticated 
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('loginPage'))
    u = retrieveUser(request)    
    l=[]
    if(isinstance(u,CommercialUser)):
        l=CasualUser.objects.all()
    elif(isinstance(u,PremiumUser)):
        l=u.friends.all()
    buttonlist=["Select","Go_Back"]
    attr = {'list':l,'title':'Select a person to send message','buttonlist':buttonlist,'responseType':'single','returnFunction':"getSendPrivateMessageRequest1" }
    return display_Menu(attr,request)

def getResponseList(request):
    # # check if user is authenticated 
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('loginPage'))
    responseType = request.POST['responseType']
    u = retrieveUser(request)
    indexList = []
    if('indexList' in request.POST.keys()):
        if (responseType=='single') :        
            indexList = getIndexList(request.POST['indexList'])    
        elif(responseType=='multi') :
            indexList = getIndexList_Mutli(request.POST.getlist('indexList')) 

        return(indexList)
    else:
        return(indexList)

def getFriendRequestResponse(request):
    # # check if user is authenticated 
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('loginPage'))
    u = retrieveUser(request)
    buttonlist=['Send_request',"Go_back"]
    u = retrieveUser(request)    
    l=CasualUser.objects.all()
    m2=u.friends.all()
    l2=[]
    for element in l:
        if element not in m2 and element.pk!=u.pk:
            l2.append(element)
    
    responseList=getResponseList(request)
    button= request.POST['submit']
    if(button=='Send_request'):
        for fr in responseList:
            u.error = u.send_friend_request(l2[fr].pk)
        u.save()
        return HttpResponseRedirect(reverse('mainPage'))
    elif(button=="Go_back"):
        return HttpResponseRedirect(reverse('mainPage'))
    

def getMoneyRequestResponse1(request,responseList):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('loginPage'))
    u = retrieveUser(request)    
    try:
        u.intHolder=responseList[0].pk
    except:
        u.error = 'Select a money request'
        u.save()
        return HttpResponseRedirect(reverse('mainPage'))
    u.save()
    return enterMoneytoSend(request)

def getMoneyRequestResponse2(request):
    # # check if user is authenticated 
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('loginPage'))
    u = retrieveUser(request)
    amount=request.POST['text']
    try:
        amount = float(amount)
    except ValueError:
        u.error = 'Amount not a float number'
        u.save()
        return HttpResponseRedirect(reverse('mainPage'))
    u.error = u.send_money(amount,u.intHolder)
    u.save()
    return HttpResponseRedirect(reverse('mainPage'))

def getMRADResponse(request):
    # # check if user is authenticated 
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('loginPage'))
    u = retrieveUser(request)
    responseList=getResponseList(request)
    l=u.money_requests.all()
    button=request.POST['submit']
    if(button == "Accept"):
        for mrequest in responseList:
            u.error = u.accept_money(l[mrequest].pk)
        u.save()
        return HttpResponseRedirect(reverse("mainPage"))
    elif(button=="Decline"):
        for mrequest in responseList:
            u.error = u.reject_money(l[mrequest].pk)
        u.save()
        return HttpResponseRedirect(reverse("mainPage"))
    elif(button=="Go_Back"):
        return HttpResponseRedirect(reverse("mainPage"))


def getFRADResponse(request):
    # # check if user is authenticated 
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('loginPage'))
    u = retrieveUser(request)
    l=u.friend_requests.all()
    responseList=getResponseList(request)
    button= request.POST['submit']
    if(button == "Accept"):
        for frequest in responseList:
            u.error = u.accept_friend_request(l[frequest].pk)
        u.save()
        return HttpResponseRedirect(reverse('mainPage'))
    elif(button=="Decline"):
        for frequest in responseList:
            u.error = u.reject_friend_request(l[frequest].pk)
        u.save()        
        return HttpResponseRedirect(reverse('mainPage'))
    elif(button=="Go_Back"):
        return HttpResponseRedirect(reverse('mainPage'))

def viewFriendProfile(friend,request):
    # # check if user is authenticated 
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('loginPage'))
    infoList=[]
    u = retrieveUser(request)
    u.intHolder=friend.pk
    u.save()
    timeline = Timeline.objects.get(timeline_of=friend)
    postList=[str(post) for post in timeline.posts.all()]
    enablePost = friend.others_can_post
    if(friend.others_can_see_dob==True):
        infoList.append("DOB:- "+str(friend.date_of_birth))
    if(friend.others_can_see_email==True):
        infoList.append("E-mail:- "+str(friend.email_id))
    attr={'name':friend.username,'enablePost':enablePost,'infoList':infoList,'postList':postList,'Error':u.error}
    u.error = ''
    u.save()
    return(render(request,"mainapp/userProfile.html",attr))
        

def getFLResponse(request):
    # # check if user is authenticated 
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('loginPage'))
    u = retrieveUser(request)
    responseList=getResponseList(request)
    l=u.friends.all()
    button= request.POST['submit']
    if(button=="View_Profile/Timeline"):
        try:
            return viewFriendProfile(l[responseList[0]],request)
        except IndexError:
            u.error = 'Friend not selected'
            u.save()
            return HttpResponseRedirect(reverse('mainPage'))
    elif(button=="Unfriend"):
        try:
            u.error = u.unfriend(l[responseList][0].pk)
            u.save()
        except IndexError:
            u.error = 'Friend not selected'  
            u.save()
        return HttpResponseRedirect(reverse("mainPage"))
    elif(button=="Send_Money_Request"):
        otp_mail = TOTPVerification()
        generated_token = otp_mail.generate_token()
        # print(generated_token)
        request.session['token']=generated_token
        mail_subject = 'InstaBook: Verify OTP for Transaction'
        message = render_to_string('login/acc_active_email.html', {
            'username': u.username,
            'otp': generated_token,
        })

        email = EmailMessage(
            mail_subject, message, to=[u.email_id]
        )
        email.send()
        try:
            return render(request,'mainapp/otp_page.html',context={"Msg": "Enter OTP below!","username":l[responseList[0]].username,"userCat":l[responseList[0]].category})
        except IndexError:
            u.error = 'Friend not selected'
            u.save()
            return HttpResponseRedirect(reverse('mainPage'))
    elif(button=="Post_on_timeline"):
        pass
    elif(button=="Go_Back"):
        return HttpResponseRedirect(reverse("mainPage"))
    
def verify_otp_mainapp(request):
    # # check if user is authenticated 
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('loginPage'))
    u = retrieveUser(request)
    token=None    
    otp = request.POST['otp']
    username = request.POST['username']
    userCat= request.POST['userCat']
    if('token' in request.session):
        token=request.session['token']
    else:
        return HttpResponseRedirect(reverse("mainPage"))
    try:
        otp=int(otp)
   
    except ValueError:
        del request.session['token']
        return HttpResponseRedirect(reverse("mainPage"))
    if (otp==int(token)):
        del request.session['token']
        user=None
        if (userCat=='commercial'):
            user=CommercialUser.objects.get(username=username)
        elif(userCat=='premium'):
            user=PremiumUser.objects.get(username=username)
        elif(userCat=='casual'):
            user=CasualUser.objects.get(username=username)
        return getMoneyRequestResponse1(request,[user])
    else :
        return render(request,'mainapp/otp_page.html',context={"Msg": "Wrong OTP!","username":username,"userCat":userCat})

def getAccept_MoneyRequestResponse(request):
    # # check if user is authenticated 
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('loginPage'))
    u = retrieveUser(request)
    responseList=getResponseList(request)
    l = u.money_requests.all()
    try:
        u.error = u.accept_money(l[responseList][0].pk)
        u.save()
    except:
        u.error = 'Money request not selected'
        u.save()
    return HttpResponseRedirect(reverse('mainPage'))

def getDecline_MoneyRequestResponse(request):
    # # check if user is authenticated 
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('loginPage'))
    u = retrieveUser(request)
    l = u.money_requests.all()
    responseList=getResponseList(request)
    try:
        u.error = u.reject_money(l[responseList[0]].pk)
        u.save()
    except IndexError:
        u.error = 'Money request not selected'
        u.save()
    return HttpResponseRedirect(reverse('mainPage'))

def getPostOnOwnTimelineResponse(request):
    # # check if user is authenticated 
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('loginPage'))
    u = retrieveUser(request)
    text = request.POST['potText']
    text = text[:500]
    u.error = u.post_on_own_timeline(text)
    u.save()
    return HttpResponseRedirect(reverse('mainPage'))

def getPostOnOtherTimelineResponse1(request):
    # # check if user is authenticated 
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('loginPage'))
    responseList=getResponseList(request)
    u = retrieveUser(request)
    l=u.friends.all()
    try:
        u.intHolder=l[responseList[0]].pk
    except:
        u.error = 'Select a friend first'
        u.save()
        return HttpResponseRedirect(reverse('mainPage'))
    u.save()
    attr={'title':"Enter Post Content",'submitText':"Post",'returnFunction':'getPostOnOtherTimelineResponse2'}
    return display_textbox(attr,request)

def getPostOnOtherTimelineResponse2(request):
    # # check if user is authenticated 
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('loginPage'))
    u = retrieveUser(request)    
    text = request.POST['potText']
    text = text[:500]
    u.post_on_other_timeline(u.intHolder,text)
    return viewFriendProfile(CasualUser.objects.get(pk=u.intHolder),request)    

def getSendPrivateMessageRequest1(request):
    # # check if user is authenticated 
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('loginPage'))
    u = retrieveUser(request)    
    buttonlist=["Select","Go_Back"]
    button=request.POST['submit']
    l=[]
    if(isinstance(u,CommercialUser)):
        l=CasualUser.objects.all()
    elif(isinstance(u,PremiumUser)):
        l=u.friends.all()
    if(button==buttonlist[0]):
        responseList=getResponseList(request)
        try:
            u.intHolder=l[responseList[0]].pk
        except IndexError:
            u.error = 'Select a user'
            u.save()
            return HttpResponseRedirect(reverse('mainPage'))
        u.save()
        attr={'title':"Enter Messsage",'submitText':"Send",'returnFunction':'getSendPrivateMessageRequest2'}
        return display_textbox(attr,request)
    else:
        return HttpResponseRedirect(reverse('mainPage'))    


def getSendPrivateMessageRequest2(request):
    # # check if user is authenticated 
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('loginPage'))
    u = retrieveUser(request)    
    text = request.POST['text']
    text = text[:500]
    u.error = u.send_message(u.intHolder,text)
    u.save()
    return HttpResponseRedirect(reverse('mainPage'))   

def getPageResponse(request):
    # # check if user is authenticated 
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('loginPage'))
    u = retrieveUser(request)
    content=request.POST['text']
    fk=Page.objects.filter(admin=u)
    if(fk.exists()):
        # fk[0].content=content
        # fk[0].save()
        u.error='You have already created a page'
        u.save()
    else:
        u.error = u.create_page(content)
        u.save()
    return HttpResponseRedirect(reverse("mainPage"))

def createPage(request):
    # # check if user is authenticated 
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('loginPage'))
    u = retrieveUser(request)    
    attr={'title':"Enter content for the page",'submitText':"Create Page",'returnFunction':"getPageResponse"}
    return display_textbox(attr,request)

# display text box
def display_textbox(attr,request) :
    # # check if user is authenticated 
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('loginPage'))
    u = retrieveUser(request)

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
    # # check if user is authenticated 
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('loginPage'))
    u = retrieveUser(request)
    attr={'title':"Enter amount to deposit",'submitText':"Deposit",'returnFunction':'getDepositResponse'}
    return display_textbox(attr,request)

def enterMoneytoSend(request):
    # # check if user is authenticated 
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('loginPage'))
    u = retrieveUser(request)    
    attr={'title':"Enter amount to send",'submitText':"Send",'returnFunction':'getMoneyRequestResponse2'}
    return display_textbox(attr,request)

def getDepositResponse(request):
    # # check if user is authenticated 
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('loginPage'))
    u = retrieveUser(request)
    amount=request.POST['text']
    try:
        amount = float(amount)
    except ValueError:
        u.error = 'Amount not a floating point number'
        u.save()
        return HttpResponseRedirect(reverse('mainPage'))
    u.error = u.deposit_money(amount)
    u.save()
    return HttpResponseRedirect(reverse('mainPage'))

# def viewContentlist(attr,request):
#     # check if user is authenticated 
#     if not request.user.is_authenticated:
#         return HttpResponseRedirect(reverse('loginPage'))
#     u = retrieveUser(request)    
#     title=attr['title']
#     modelList=attr['list']
#     contentList=[]
#     for model in modelList :
#         contentList.append(str(model))
#     print(contentList,"-----------------------------------")
#     context = {
#         "contentList" : contentList,
#         "title": title,
#     }
#     return render(request,"mainapp/contentList.html",context=context)

def privacySettings(request):
    # # check if user is authenticated 
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('loginPage'))
    u = retrieveUser(request)    
    buttonList=["Confirm_Settings","Go_Back"]
    privacyList=[]
    if(u.others_can_post):
        privacyList.append(menuItem("Disallow others to post on your timeline",1))
    else:
        privacyList.append(menuItem("Allow others to post on your timeline",1))
    
    if(u.others_can_see_friends):
        privacyList.append(menuItem("Disallow others to see your friends",2))
    else:
        privacyList.append(menuItem("Allow others to see your friends",2))
    
    if(u.others_can_see_email):
        privacyList.append(menuItem("Disallow others to see your email",3))
    else:
        privacyList.append(menuItem("Allow others to see your email",3))
    
    if(u.others_can_see_dob):
        privacyList.append(menuItem("Disallow others to see your DOB",4))
    else:
        privacyList.append(menuItem("Allow others to see your DOB",4))

    l=privacyList
    attr={'title':"Change your privacy settings here",'buttonlist':buttonList,'list':l,'responseType':'multi','returnFunction':"getPrivacyResponse"}
    return display_Menu(attr,request)

def getPrivacyResponse(request):
    # # check if user is authenticated 
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('loginPage'))
    u = retrieveUser(request)
    button=request.POST['submit']
    responseList=getResponseList(request)
    if(button=="Go_Back"):
        return HttpResponseRedirect(reverse("mainPage"))
    elif(button=="Confirm_Settings"):
        for r in responseList:
            print(str(r))
            if(r==0):
                u.others_can_post=not u.others_can_post
            elif(r==1):
                u.others_can_see_friends=not u.others_can_see_friends
            elif(r==2):
                u.others_can_see_email=not u.others_can_see_email
            elif(r==3):
                u.others_can_see_dob=not u.others_can_see_dob
        u.save()
        u.error = 'Privacy settings changed'
        u.save()
        return HttpResponseRedirect(reverse("mainPage"))



# def viewMyPosts(request):
#     # # check if user is authenticated 
#     if not request.user.is_authenticated:
#         return HttpResponseRedirect(reverse('loginPage'))
#     u = retrieveUser(request)
#     mytimeline=Timeline.objects.get(timeline_of=u)
#     posts=mytimeline.posts.all()
#     attr = {
#         "list":posts,
#         "title":"Posts on your timline",
#     }
#     return viewContentlist(attr,request)

# def viewFriendsPost(request):
#     # # check if user is authenticated 
#     if not request.user.is_authenticated:
#         return HttpResponseRedirect(reverse('loginPage'))
#     u = retrieveUser(request)    
#     l=u.friends.all()
#     attr = {'list':l,'title':'Select friend','submitText':'Select','responseType':'single','returnFunction':"getViewPostOfFriendResponse" }
#     return display_Menu(attr,request)

def viewPages(request):
    # # check if user is authenticated 
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('loginPage'))
    u = retrieveUser(request)    
    l=Page.objects.all()
    buttonlist=["View","Go_back"]
    attr={'title':"Select a page to view",'buttonlist':buttonlist,'list':l,'responseType':'single','returnFunction':"getVPResponse"}
    return display_Menu(attr,request)

def getVPResponse(request):
    # # check if user is authenticated 
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('loginPage'))
    u = retrieveUser(request)    
    button=request.POST['submit']
    if(button=="Go_back"):
        return HttpResponseRedirect(reverse("mainPage"))
    elif(button=="View"):
        rList=getResponseList(request)
        try:
            r=rList[0]
            l2=Page.objects.all()
            r=l2[r]
        except IndexError:
            u.error = 'Page not selected'
            u.save()
            return HttpResponseRedirect(reverse("mainPage"))
        # print(r)
        attr={'username':r.admin,'content':r.Content,'Error':u.error}
        try:
            u.error = ''
            u.save()
            return render(request,"mainapp/page.html",attr)
        except IndexError:
            u.error = 'Page not selected'
            u.save()
            return HttpResponseRedirect(reverse('mainPage'))

# def getViewPostOfFriendResponse(request):
#     # # check if user is authenticated 
#     if not request.user.is_authenticated:
#         return HttpResponseRedirect(reverse('loginPage'))
#     u = retrieveUser(request)    
#     responseList=getResponseList(request)
#     l=u.friends.all()
#     try:
#         friend = l[responseList[0]]
#     except:
#         u.error = 'friend not selected'
#         u.save()
#         return HttpResponseRedirect(reverse("mainPage"))
#     timeline = Timeline.objects.get(timeline_of=friend)
#     posts=timeline.posts.all()
#     attr = {
#         "list":posts,
#         "title":"Posts on "+ friend.username +" timline",
#     }
#     return viewContentlist(attr,request)

def textForm_Multi(attr,request):
    # # check if user is authenticated 
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('loginPage'))
    u = retrieveUser(request)    
    return render(request,"mainapp/textForm_multiple.html",attr)


def createGroup(request):
    # # check if user is authenticated 
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('loginPage'))
    u = retrieveUser(request)    
    keys = ['Enter_Group_Name','Enter_price_for_each_member']
    buttonlist = ['create_group']
    attr= {
        'keys':keys,
        'title':'Create Group',
        'returnFunction':'getcreateGroupResponse',
        'buttonlist':buttonlist,
    }
    return textForm_Multi(attr,request)

def getcreateGroupResponse(request):
    # # check if user is authenticated 
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('loginPage'))
    u = retrieveUser(request)
    grpname = request.POST['Enter_Group_Name']
    price = request.POST['Enter_price_for_each_member']
    try:
        price = float(price)
    except ValueError:
        u.error = 'Price is not float'
        u.save()
        return HttpResponseRedirect(reverse('mainPage'))
    u.error = u.create_group(grpname,True,price)
    u.save()
    return HttpResponseRedirect(reverse("mainPage"))

def viewGroups(request):
    # # check if user is authenticated 
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('loginPage'))
    u = retrieveUser(request)    
    grps = Group.objects.all()
    buttonlist = ['View_Group','Go_Back']
    attr={'title':"Select a group to view",'buttonlist':buttonlist,'list':grps,'responseType':'single','returnFunction':"getVGResponse"}
    return display_Menu(attr,request)

def viewJR(request):
    # # check if user is authenticated 
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('loginPage'))
    u = retrieveUser(request)    
    grp=Group.objects.get(pk=u.intHolder)
    buttonlist=['Accept','Reject','Go_Back']
    l=grp.join_requests.all()
    attr={'title':"Select join requests to reject/accept",'list':l,'buttonlist':buttonlist,
    'responseType':'multi','returnFunction':"getVJRResponse"}
    return display_Menu(attr,request)

def getVJRResponse(request):
    # # check if user is authenticated 
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('loginPage'))
    u = retrieveUser(request)
    button=request.POST['submit']
    grp=Group.objects.get(pk=u.intHolder)
    if(button=="Go_Back"):
        return(getVGResponse(request,Group.objects.get(pk=u.intHolder)))
    else:
        rList=getResponseList(request)
        l=grp.join_requests.all()
        if(button=="Accept"):
            for r in rList:
                u.error=u.accept_join_request(grp.pk,l[r].pk)
                u.save()
        if(button=="Reject"):
            for r in rList:
                u.error=u.reject_join_request(grp.pk,l[r].pk)
                u.save()
        return(getVGResponse(request,Group.objects.get(pk=u.intHolder)))


def groupPS(request):
    # # check if user is authenticated 
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('loginPage'))
    u = retrieveUser(request)    
    s3=""
    s1=""
    s2=""
    grp=Group.objects.get(pk=u.intHolder)
    b=grp.can_send_join_requests
    s1="(Current:- "+str(grp.price)+" )"
    s2="(Current:- "+grp.name+" )"
    if(b):
        s3="(Currently users can send join requests)"
    else:
        s3="(Currently users cannot send join requests)"

    l=[menuItem("Change Price"+s1,1),menuItem("Change Name"+s2,2),menuItem("Toggle Join Setting "+s3,3)]
    
    buttonlist=["Change_Setting","Go_Back"]
    attr={'title':"Select a setting to change",'list':l,'buttonlist':buttonlist,'responseType':'single','returnFunction':"getGSResponse"}
    return display_Menu(attr,request)

def getGSResponse(request):
    # # check if user is authenticated 
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('loginPage'))
    u = retrieveUser(request)    
    grp=Group.objects.get(pk=u.intHolder)
    button=request.POST['submit']
    if(button=="Go_Back"):
        return(getVGResponse(request,Group.objects.get(pk=u.intHolder)))
    elif(button=="Change_Setting"):
        rList=getResponseList(request)
        try:
            resp=rList[0]
        except IndexError:
            u.error = 'No option selected'
            u.save()
            return HttpResponseRedirect(reverse("mainPage"))
        if(resp==0):
            attr={'title':"Enter new price",'submitText':"Change Price",'returnFunction':"getGCPResponse"}
            return display_textbox(attr,request)
        elif(resp==1):
            attr={'title':"Enter new name",'submitText':"Change Name",'returnFunction':"getGCNResponse"}
            return display_textbox(attr,request)
        elif(resp==2):
            u.change_join_request_settings(grp.pk,not grp.can_send_join_requests)
            return(getVGResponse(request,Group.objects.get(pk=u.intHolder)))


def getGCNResponse(request):
    # # check if user is authenticated 
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('loginPage'))
    u = retrieveUser(request)    
    name=request.POST['text']
    grp=Group.objects.get(pk=u.intHolder)
    print(u.change_name(grp.pk,name))
    return(getVGResponse(request,Group.objects.get(pk=u.intHolder)))

def getGCPResponse(request):
    # # check if user is authenticated 
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('loginPage'))
    u = retrieveUser(request)    
    price=request.POST['text']
    grp=Group.objects.get(pk=u.intHolder)
    print(u.change_price(grp.pk,float(price)))
    return(getVGResponse(request,Group.objects.get(pk=u.intHolder)))



def getPostOnGroupResponse(request):
    # # check if user is authenticated 
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('loginPage'))
    u = retrieveUser(request)    
    message=request.POST['pogText']
    print(u.send_message_on_group(u.intHolder,message))
    return(getVGResponse(request,Group.objects.get(pk=u.intHolder)))

def joinGroup(request):
    # # check if user is authenticated 
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('loginPage'))
    u = retrieveUser(request)
    grp=Group.objects.get(pk=u.intHolder)
    print(u.send_join_request(u.intHolder))
    return(HttpResponseRedirect(reverse("mainPage")))

def getVGResponse(request,grp=1):
    # # check if user is authenticated 
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('loginPage'))
    u = retrieveUser(request)    
    button=1
    if(grp==1):
        button = request.POST['submit']
    if (grp==1 and button=='Go_Back'):
        return HttpResponseRedirect(reverse("mainPage"))
    elif(grp!=1 or button=='View_Group'):
        if(grp==1):
            responseList = getResponseList(request)
            try:
                grp = responseList[0]
                l1=Group.objects.all()
                grp=l1[grp]
            except:
                u.error = 'Group not selected'
                u.save()
                return HttpResponseRedirect(reverse("mainPage"))
        u.intHolder=grp.pk
        u.save()
        if (grp.admin.pk==u.pk):
            attr={'groupTitle':grp.name,'groupAdmin':str(grp.admin),
            'messageList':[str(m) for m in grp.messages.all()],
            'memberList':[str(mem) for mem in grp.members.all()], 'Error':u.error}
            try:
                u.error = ''
                u.save()
                return render(request,"mainapp/adminGroup.html",attr)
            except IndexError:
                u.error = 'Group not selected'
                u.save()
                return HttpResponseRedirect(reverse('mainPage'))
        elif(u.pk in [l.pk for l in grp.members.all()]):
            attr={'groupTitle':grp.name,'groupAdmin':str(grp.admin),
            'messageList':[str(m) for m in grp.messages.all()],
            'memberList':[str(mem) for mem in grp.members.all()], 'Error':u.error}
            try:
                u.error = ''
                u.save()
                return render(request,"mainapp/joinedGroup.html",attr)
            except:
                u.error = 'Group not selected'
                u.save()
                return HttpResponseRedirect(reverse('mainPage'))
        else:
            isRSent=False
            canJoin=False
            if(u.pk in [l.pk for l in grp.join_requests.all()]):
                isRSent=True
            if(grp.can_send_join_requests):
                canJoin=True
            print(isRSent)
            attr={'groupTitle':grp.name,'groupAdmin':str(grp.admin),'groupAdmin':str(grp.admin),'sent':isRSent,'canJoin':canJoin,'price':grp.price, 'Error':u.error}
            try:
                u.error = ''
                u.save()
                return render(request,"mainapp/unjoinedGroup.html",attr)
            except IndexError:
                u.error = 'Group Not selected'
                u.save()
                return HttpResponseRedirect(reverse('mainPage'))
            return render(request,"mainapp/unjoinedGroup.html",attr)


def search_friend(request):
    # # check if user is authenticated 
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('loginPage'))
    u = retrieveUser(request)    
    attr = {'title':"Enter friend name",'submitText':"Search",'returnFunction':"getFriendSearchResponse"}
    return display_textbox(attr,request)

def search_group(request):
    # # check if user is authenticated 
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('loginPage'))
    u = retrieveUser(request)    
    attr = {'title':"Enter group name",'submitText':"Search",'returnFunction':"getGroupSearchResponse"}
    return display_textbox(attr,request)

def getFriendSearchResponse(request):
    # # check if user is authenticated 
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('loginPage'))
    u = retrieveUser(request)
    text = request.POST['text']
    userlist = u.friends.filter(username=text)
    if (len(userlist)==0):
        u.error='No friend with username: '+text
        u.save()
        return HttpResponseRedirect(reverse('mainPage'))
    buttonlist=["View_Profile/Timeline","Unfriend","Send_Money_Request","Go_Back"]
    attr={'list':userlist,'title':'Search Results','buttonlist':buttonlist,'responseType':'single','returnFunction':"getFLResponse"}    
    return display_Menu(attr,request)

def getGroupSearchResponse(request):
    # # check if user is authenticated 
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('loginPage'))
    u = retrieveUser(request)
    text = request.POST['text']
    grplist = Group.objects.filter(name=text)
    if (len(grplist)==0):
        u.error='No group with name: '+text
        u.save()
        return HttpResponseRedirect(reverse('mainPage'))
    buttonlist = ['View_Group','Go_Back']
    attr={'title':"Select a group to view",'buttonlist':buttonlist,'list':grplist,'responseType':'single','returnFunction':"getVGResponse"}
    return display_Menu(attr,request)
