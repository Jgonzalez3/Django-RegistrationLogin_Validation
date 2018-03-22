from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from time import gmtime, strftime
from django.utils.crypto import get_random_string
from .models import Users
import bcrypt, re

def index(request):
    return render(request, "login_reg/index.html")

def register(request):
    if request.method =='POST':
        request.session["firstname"] = request.POST["firstname"]
    hash1 = bcrypt.hashpw(request.POST["password"].encode(), bcrypt.gensalt())
    print "hash1", hash1
    errors = Users.objects.basic_validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect("/")
    else:
        user = Users.objects.create(first_name = request.POST["firstname"], last_name = request.POST["lastname"], email = request.POST["email"], birthdate = request.POST["birthdate"], password = hash1)
        user.save()
        return redirect("/login_reg/success")

def login(request):
    loginerrors = Users.loginobjects.login_validator(request.POST)
    user = Users.objects.filter(email__contains=request.POST["loginemail"])
    for fname in user:
        request.session["firstname"] = fname.first_name
    if len(loginerrors):
        for tag, loginerror in loginerrors.iteritems():
            messages.error(request, loginerror, extra_tags=tag)
        return redirect("/")
    else:
        return redirect("/login_reg/success")
def success(request):
    return render(request, "login_reg/success.html")