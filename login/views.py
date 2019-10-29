from django.shortcuts import render, render_to_response, HttpResponse, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse, resolve
from mainapp.models import CasualUser, PremiumUser, CommercialUser
from django.contrib.auth import authenticate, login, logout, models, logout
import json
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from .utils import TOTPVerification
from .forms import *

otp_mail = TOTPVerification()

username = None
password = None
email_reg = None
category = None
dob = None

# show login Page


def loginPage(request):
    return render(request, "login/loginPage.html")

# authentication


def authentication(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect(reverse('displayMainMenu'))
    else:
        return render(request, 'login/loginPage.html', context={'Msg': 'Login Failed'})

# logout


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('loginPage'))

#  show sign up form


def forgotPass(request):
    return render(request, 'login/forget.html', context={'from': forgotForm})


def signUpForm(request):
    return render(request, "login/SignUpForm.html", context={'form': SignUpForm})


def sendOTP(request):
    global username
    form = forgotForm(request.POST)
    if(form.is_valid()):
        username = form.cleaned_data['username']
        user = CasualUser.objects.filter(username=username)
        if not user.exists():
            return render(request, 'login/forget.html', context={'from': forgotForm, 'errors': 'user does not exist'})

        generated_token = otp_mail.generate_token()
        user = user[0]
        email_reg = user.email_id

        mail_subject = 'InstaBook: Verify OTP'
        message = render_to_string('login/acc_active_email.html', {
            'username': username,
            'otp': generated_token,
        })

        email = EmailMessage(
            mail_subject, message, to=[email_reg]
        )
        email.send()

        return render(request, "login/otp_page.html", context={"Msg": "Enter OTP below!", 'redirect_url': 'verify'})
    else:
        return render(request, 'login/forget.html', context={'from': forgotForm, 'errors': form.errors})


def changePass(request):
    otp = request.POST['otp']
    if otp_mail.verify_token(otp):
        user = CasualUser.objects.filter(username=username)
        

def createUser(request):
    global username
    global password
    global email_reg
    global category
    global dob

    form = SignUpForm(request.POST)
    # print(form.errors)
    if(form.is_valid()):

        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']
        email_reg = form.cleaned_data['email']
        category = form.cleaned_data['category']
        dob = form.cleaned_data['date_of_birth']

        generated_token = otp_mail.generate_token()
        # print(generated_token)

        mail_subject = 'InstaBook: Verify OTP'
        message = render_to_string('login/acc_active_email.html', {
            'username': username,
            'otp': generated_token,
        })

        email = EmailMessage(
            mail_subject, message, to=[email_reg]
        )
        email.send()

        return render(request, "login/otp_page.html", context={"Msg": "Enter OTP below!", 'redirect_url': 'otp'})
    else:
        return render(request, "login/SignUpForm.html", context={'form': SignUpForm, 'errors': form.errors})


def otp_page(request):
    global username
    global password
    global email_reg
    global category
    global dob

    if (username is None):
        return HttpResponseRedirect(reverse('loginPage'))

    otp = request.POST['otp']
    print(otp)
    if otp_mail.verify_token(otp):
            # create django user model instance

        # Create mainapp user model instance
        user = None
        if (category == "casual"):
            user = CasualUser.create(
                username=username, email_id=email_reg, dob=dob)
            newUser = models.User.objects.create_user(
                username, email_reg, password)
        elif(category == "premium"):
            return render(request, "login/selectPlan.html", context={"Msg": "Choose plan", 'form': PlanForm})
        elif(category == "commercial"):
            user = CommercialUser.create(
                username=username, email_id=email_reg, dob=dob)
            newUser = models.User.objects.create_user(
                username, email_reg, password)
        username = None
        password = None
        email_reg = None
        category = None
        dob = None

        return HttpResponseRedirect(reverse('loginPage'))
    else:

        return render(request, "login/otp_page.html", context={"Msg": "Wrong OTP!", 'redirect_url': 'otp'})


def choosePlan(request):
    form = PlanForm(request.POST)
    if(form.is_valid()):
        plan = form.cleaned_data['plan']
        user = PremiumUser.create(
            username=username, plan=plan, email_id=email_reg, dob=dob)
        newUser = models.User.objects.create_user(
            username, email_reg, password)
        return HttpResponseRedirect(reverse('loginPage'))
