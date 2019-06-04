import json
from django.shortcuts import render, redirect
import websocket
from django.contrib import messages

import unittest
#import json



# Create your views here.
def signup(request):
    if(request.method == "POST"):
        args =request.POST
        if args['username']!='' and args['psw'] == args['psw-repeat']:
            result = {'action':'signup', 'username': args['username'] , 'password': args['psw']}
            if(result['success']== True):
                messages.info(request, 'Your password has been changed successfully!')
                return redirect('/')
            else:
                messages.info(request, 'Your password has been changed unsuccessfully!')

    render(request, 'accounts/signup.html', args)
    return redirect('/')

    args = {'form': 1}
    return render(request, 'accounts/signup.html', args)