import uuid
import sys
#from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login, logout as auth_logout
#import login as auth_login
from django.core.mail import send_mail
from django.shortcuts import redirect, render
from accounts.authentication import PasswordlessAuthenticationBackend
from django.contrib import messages,auth
from django.urls import reverse
from accounts.models import Token

import pdb
from accounts.models import Token

#def send_login_email(request):
    #email = request.POST['email']
    #uid = str(uuid.uuid4())
    #Token.objects.create(email=email, uid=uid)
    #print('saving uid', uid, 'for email', email, file=sys.stderr)
    #url = request.build_absolute_uri(f'/accounts/login?uid={uid}')
    #send_mail(
    #    'Your login link for Superlists',
    #    f'Use this link to log in:\n\n{url}',
    #    'noreply@superlists',
    #    [email],
    #)
    #return render(request, 'login_email_sent.html')
    #return redirect('/')

def login(request):
    login_id = request.GET.get('token')
    user = PasswordlessAuthenticationBackend().authenticate(uid=login_id)
    #user = auth.authenticate(uid=login_id)
    #pdb.set_trace()
    if user is not None:
        auth_login(request,user)
        #auth.login(request,user)
    return redirect('/')
    
def logout(request):
    auth_logout(request)
    return redirect('/')

def send_login_email(request):
    email = request.POST['email']
    token= Token.objects.create(email=email)
    url = request.build_absolute_uri(  
        reverse('login') + '?token=' + str(token.uid)
    )
    message_body = f'Use this link to log in:\n\n{url}'
    print(type(send_mail))
    send_mail(
        'Your login link for Superlists',
        message_body,
        'noreply@superlists',
        [email]
    )
    messages.success(
        request,
        "Check your email, we've sent you a link you can use to log in."
    )
    return redirect('/')
