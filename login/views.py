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
from .models import TempUser


# username = None
# password = None
# email_reg = None
# category = None
# dob = None

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
        return HttpResponseRedirect(reverse('mainPage'))
    else:
        return render(request, 'login/loginPage.html', context={'Msg': 'Login Failed'})

# logout


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('loginPage'))

#  show sign up form


def signUpForm(request):
    # users = CasualUser.objects.all()
    # Names_List = []
    # for user in users:
    #     Names_List.append(user.username)
    # context = {
    #     "len": len(Names_List),
    #     "names": json.dumps(Names_List),
    # }
    return render(request, "login/SignUpForm.html", context={'form': SignUpForm})

# create user


def createUser(request):
    # global username
    # global password
    # global email_reg
    # global category
    # global dob

    form = SignUpForm(request.POST)
    # print(form.errors)
    if(form.is_valid()):

        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']
        email_reg = form.cleaned_data['email']
        category = form.cleaned_data['category']
        dob = form.cleaned_data['date_of_birth']

        otp_mail = TOTPVerification()

        generated_token = otp_mail.generate_token()
        # print(generated_token)

        request.session['token'] = generated_token

        mail_subject = 'InstaBook: Verify OTP'
        message = render_to_string('login/acc_active_email.html', {
            'username': username,
            'otp': generated_token,
        })

        email = EmailMessage(
            mail_subject, message, to=[email_reg]
        )
        email.send()

        tempUser = TempUser(username=username, password=password,
                            email_reg=email_reg, category=category, dob=dob)
        tempUser.save()
        pr = tempUser.pk
        request.session['user'] = pr

        return render(request, "login/otp_page.html", context={"Msg": "Enter OTP below!"})
    else:
        return render(request, "login/SignUpForm.html", context={'form': SignUpForm, 'errors': form.errors})


def otp_page(request):

    token = None

    if('user' in request.session):
        pr = request.session['user']
    else:
        return HttpResponseRedirect(reverse('loginPage'))

    if('token' in request.session):
        token = request.session['token']

    else:
        return HttpResponseRedirect(reverse('loginPage'))

    user1 = TempUser.objects.get(pk=pr)

    otp = request.POST['otp']

    try:
        otp = int(otp)
    except ValueError:
        return HttpResponseRedirect(reverse('loginPage'))

    if int(token) == otp:
        # if True:
            # create django user model instance

        # Create mainapp user model instance
        del request.session['token']
        user = None
        if (user1.category == "casual"):
            user = CasualUser.create(
                username=user1.username, email_id=user1.email_reg, dob=user1.dob)
            newUser = models.User.objects.create_user(
                user1.username, user1.email_reg, user1.password)
            del request.session['user']
            user1.delete()
        elif(user1.category == "premium"):
            return render(request, "login/selectPlan.html", context={"Msg": "Choose plan", 'form': PlanForm})
        elif(user1.category == "commercial"):
            user = CommercialUser.create(
                username=user1.username, email_id=user1.email_reg, dob=user1.dob)
            newUser = models.User.objects.create_user(
                user1.username, user1.email_reg, user1.password)
            del request.session['user']
            user1.delete()

        return HttpResponseRedirect(reverse('loginPage'))
    else:

        return render(request, "login/otp_page.html", context={"Msg": "Wrong OTP!"})


def choosePlan(request):
    form = PlanForm(request.POST)
    if(form.is_valid()):
        if('user' in request.session):
            pr = request.session['user']
        else:
            return HttpResponseRedirect(reverse('loginPage'))

        user1 = TempUser.objects.get(pk=pr)

        plan = form.cleaned_data['plan']
        user = PremiumUser.create(
            username=user1.username, plan=user1.plan, email_id=user1.email_reg, dob=user1.dob)
        newUser = models.User.objects.create_user(
            user1.username, user1.email_reg, user1.password)
        user1.delete()
        del request.session['user']
        return HttpResponseRedirect(reverse('loginPage'))
