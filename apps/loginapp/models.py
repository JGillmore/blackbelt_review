from __future__ import unicode_literals
import re
from django.db import models
from django.contrib import messages
import bcrypt

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]{2,}$')

class UserManager(models.Manager):
    def register(self, request, first_name, last_name, email, password, confirmpassword):
        isValid = True
        if email < 1:
            messages.add_message(request, messages.INFO,"Email cannot be blank")
            isValid = False
        elif not EMAIL_REGEX.match(email):
            messages.add_message(request, messages.INFO,'Invalid email address')
            isValid = False
        if len(first_name) < 1:
            messages.add_message(request, messages.INFO,"First Name cannot be blank")
            isValid = False
        if not NAME_REGEX.match(first_name+last_name):
            messages.add_message(request, messages.INFO,'Name cannot have numbers')
            isValid = False
        if len(last_name) < 1:
            messages.add_message(request, messages.INFO,"Last Name cannot be blank")
            isValid = False
        if password != confirmpassword:
            messages.add_message(request, messages.INFO,"Passwords do not match")
            isValid = False
        else:
            pwhash=bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        if isValid:
            try:
                temp=Users.objects.create(first_name=first_name, last_name=last_name, email=email, password=pwhash)
                return temp
            except:
                messages.add_message(request, messages.INFO,"Account already exists, please log in instead")
        return False

    def login(self, request, email, password):
        try:
            user = Users.objects.get(email=email)
            request.session['name']=user.first_name
            request.session['id']=user.id
        except:
            messages.add_message(request, messages.INFO,"Invalid login")
            return False
        if bcrypt.hashpw(password.encode(), user.password.encode()) == user.password:
            return True
        messages.add_message(request, messages.INFO,"Invalid login")
        return False


class Users(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()
