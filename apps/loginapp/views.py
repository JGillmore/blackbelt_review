from django.shortcuts import render, redirect
from .models import Users
from django.contrib import messages
from django.contrib.messages import get_messages
from django.core.urlresolvers import reverse


def index(request):
    context = {}
    if messages:
        context['messages']=get_messages(request)
    return render(request, 'loginapp/index.html', context)

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        if Users.objects.login(request,email,password):
            return redirect(reverse('books:index'))
    return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')

def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        confirmpassword = request.POST['confirmpassword']
        temp = Users.objects.register(request,first_name,last_name,email,password,confirmpassword)
        if temp:
            request.session['name']=temp.first_name
            request.session['id']=temp.id
            return redirect(reverse('books:index'))
        return redirect('/')
