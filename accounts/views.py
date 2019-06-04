import json
from django.shortcuts import render, redirect
import websockets
from django.contrib import messages

import unittest
#import json


# Create your views here.
def signup(request):
    if request.method == "POST":
        args = request.POST
        if args['username'] != '' and args['psw'] == args['psw-repeat']:
            result = {'action':'signup', 'username': args['username'], 'password': args['psw']}
            if result['success']:
                messages.info(request, 'Your password has been changed successfully!')
                return redirect('/')
            else:
                messages.info(request, 'Your password has been changed unsuccessfully!')

    render(request, 'accounts/signup.html', args)
    return redirect('/')

    args = {'form': 1}
    return render(request, 'accounts/signup.html', args)


def add_item_to_inventory(request):
    if request.method == "POST":
        args = request.POST
        if args['username'] != '' and args['price'] != '' and args['category'] != '':
            result = {'action': 'add_item_to_inventory',
                      'item': {'name': args['username'], 'price': args['price'], 'category': args['category']},
                      'store_name': args['storename'], 'quantity': 0}
            if result['success']:
                messages.info(request, 'Item successfully added')
                return redirect('/')
            else:
                messages.info(request, 'Item unsuccessfully added')

    render(request, 'store/add_product.html', args)
    return redirect('/')

    args = {'form': 1}
    return render(request, 'store/add_product.html', args)


def edit_item(request):
    if request.method == "POST":
        args = request.POST
        if args['username'] != '' and args['category'] != '':
            result = {'action': 'edit_product', 'itemname': args['username'], 'price': args['price'],
                      'store_name': args['storename'], 'quantity': args['quantity']}
            if result['success']:
                messages.info(request, 'Item successfully edited')
                return redirect('/')
            else:
                messages.info(request, 'Item unsuccessfully edited')

    render(request, 'store/edit_product.html', args)
    return redirect('/')

    args = {'form': 1}
    return render(request, 'store/edit_product.html', args)
