from django.shortcuts import render, render_to_response,HttpResponse, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, resolve
from mainapp.models import CasualUser, PremiumUser, CommercialUser
from django.contrib.auth import authenticate, login, logout, models, logout
import json
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from .utils import otp_mail

username = None
password = None
email_reg = None
category = None

# show login Page
def loginPage(request) :
    return render(request,"login/loginPage.html")

# authentication
def authentication(request) :
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse('user_List'))
    else:
        return HttpResponseRedirect(reverse('loginPage'))

# logout 
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('loginPage'))

#  show sign up form
def signUpForm(request):
    users = CasualUser.objects.all()
    Names_List = []
    for user in users :
        Names_List.append(user.username)
    context = {
        "len" : len(Names_List),
        "names" : json.dumps(Names_List),
    }
    return render(request,"login/SignUpForm.html",context)

# create user     
def createUser(request):
    global username
    global password
    global email_reg
    global category

    username = request.POST['username']
    password = request.POST['password']
    email_reg = request.POST['email']
    category = request.POST['category']
    
    generated_token = otp_mail.generate_token()

    mail_subject = 'InstaBook: Verify OTP'
    message = render_to_string('login/acc_active_email.html', {
        'username': username,
        'otp':generated_token,
    })
   
    email = EmailMessage(
                mail_subject, message, to=[email_reg]
    )
    email.send()
    
    return render(request,"login/otp_page.html",context={"Msg":"Enter OTP below!"})

def otp_page(request):
    global username
    global password
    global email_reg
    global category

    if (username==None) :
        return HttpResponseRedirect(reverse('loginPage'))

    otp=request.POST['otp']
    print(otp)
    if otp_mail.verify_token(otp):

        # create django user model instance
        newUser = models.User.objects.create_user(username, email_reg, password)
    
        # Create mainapp user model instance 
        user = None
        if (category=="casual"):
            user = CasualUser(username=username,category=category)
        elif(category=="premium"):
            user = PremiumUser(username=username,category=category)
        elif(category=="commercial"):
            user = CommercialUser(username=username,category=category)
        user.email_id=email_reg
        user.save()
        
        username = None
        password = None
        email_reg = None
        category = None

        return HttpResponseRedirect(reverse('loginPage'))
    else :

        return render(request,"login/otp_page.html",context={"Msg":"Wrong OTP!"})