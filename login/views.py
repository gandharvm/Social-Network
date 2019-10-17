from django.shortcuts import render, render_to_response,HttpResponse, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, resolve
from mainapp.models import CasualUser, PremiumUser, CommercialUser, User
from django.contrib.auth import authenticate, login, logout, models, logout
import json

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string

from django.contrib.auth.models import User
from django.core.mail import EmailMessage

from .models import otp_mail

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
    users = User.objects.all()
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
    username = request.POST['username']
    password = request.POST['password']
    confirmPassword = request.POST['confirmPassword']
    email_reg = request.POST['email']
    category = request.POST['category']
    newUser = models.User.objects.create_user(username, email_reg, password)
    
    # Create user model instance 
    user = None
    if (category=="casual"):
        user = CasualUser(username=username,category=category)
    elif(category=="premium"):
        user = PremiumUser(username=username,category=category)
    elif(category=="commercial"):
        user = CommercialUser(username=username,category=category)
    user.is_active = False
    user.save()
    
    generated_token = otp_mail.generate_token()

    mail_subject = 'Activate your blog account.'
    message = render_to_string('login/acc_active_email.html', {
        'user': user,
        
        
        'otp':generated_token,
        #'token':account_activation_token.make_token(user),
    })
   
    email = EmailMessage(
                mail_subject, message, to=[email_reg]
    )
    email.send()
    

    # TODO add OTP verification of email
    return render(request,"login/otp_page.html")

def otp_page(request):
    otp=request.POST['otp']
    if otp_mail.verify_token(otp):
        # user.is_active(True)
        # user.save()
        return HttpResponseRedirect(reverse('loginPage'))


