from django.shortcuts import render, redirect
from django.core.urlresolvers import reverse
from .models import *

def index(request):
    comments=Comments.objects.all().order_by('-id')[:3]
    books=Books.objects.all().order_by('title')
    context={'comments':comments,'books':books}
    return render(request, 'bookapp/index.html', context)

def add(request):
    books = Books.objects.all().order_by('author').values_list('author', flat=True).distinct()
    print books
    context = {'books':books}
    return render(request, 'bookapp/addbook.html', context)

def addbook(request):
    if request.method == 'POST':
        title = request.POST['title']
        comment = request.POST['comment']
        rating = request.POST['rating']
        if request.POST['newauthor']:
            author = request.POST['newauthor']
        else:
            author = request.POST['author']
        user = Users.objects.get(id=request.session['id'])
        book = Books.objects.create(title=title,author=author)
        Comments.objects.create(comment=comment, rating=rating, book=book, user=user)
        return redirect(reverse('books:book', kwargs={'id':book.id}))

def book(request, id):
    book = Books.objects.get(id=id)
    comments = book.bookcomments.all()
    context = {'book':book,'comments':comments}
    return render(request, 'bookapp/book.html', context)

def deletecomment(request, id):
    comment = Comments.objects.get(id=id)
    comment.delete()
    return redirect(reverse('books:index'))

def userpage(request, id):
    user=Users.objects.get(id=id)
    comments=Comments.objects.filter(user=user)
    count=0
    for comment in comments:
        count+=1
    context={'user':user,'comments':comments,'count':count}
    return render(request, 'bookapp/user.html', context)

def addcomment(request, id):
    if request.method=='POST':
        comment=request.POST['comment']
        rating=request.POST['rating']
        user = Users.objects.get(id=request.session['id'])
        book = Books.objects.get(id=id)
        Comments.objects.create(comment=comment, rating=rating, book=book, user=user)
        return redirect(reverse('books:book', kwargs={'id':id}))
