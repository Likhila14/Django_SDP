
# Create your views here.
from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render, redirect
from .forms import CreateUserForm, UserCreationForm , BookForm , ReviewForm
from django.contrib import messages
from .models import Mothersday, Register,Birthday,Anniversary
from django.db.models import Q
from django.contrib.auth import authenticate , login as log_in ,logout
from django.contrib.auth.models import User
from .models import Book,Review


def register(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data['username']
                messages.success(request ,'Account Created for' +"   " + user)
                return redirect('login')

        context = {'form':form}
        return render(request,"firstapp/register.html",context)


def login(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:

        if request.method=='POST':
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request,username=username,password=password)
            if user is not None:

                log_in(request,user)
                if request.user.is_authenticated:
                    messages.success(request, "Login Successfull!")
                return redirect('home')
            else:
                messages.warning(request ,'USERNAME OR PASSWORD IS INCORRECT')
                


        context = {}
        return render(request,"firstapp/login.html",context)



def home(request):
    bday = Birthday.objects.all()[:4]
    anni = Anniversary.objects.all()[:4]
    mom = Mothersday.objects.all()[:4]
    dict={
        'bday' : bday,
        'anni' : anni,
        'mom' : mom
    }
    return render(request,"firstapp/home.html",dict)

def contactus(request):
    return render(request, "firstapp/contact.html")
def aboutus(request):
    return render(request, "firstapp/aboutus.html")

def logoutUser(request):
    logout(request)
    messages.success(request ,'Logged Out Successfully')
    return redirect('login')

def book(request, id):
    if request.method == 'POST':
        print(request.POST)
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data['username']
            messages.success(request ,'Account Created for' +"   " + user)
            return redirect('home')
    else:
        form = BookForm()
    event = Birthday.objects.get(id=id)
    return render(request,"firstapp/book.html", {'event': event})
def abook(request, id):
    if request.method == 'POST':
        print(request.POST)
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data['username']
            messages.success(request ,'Account Created for' +"   " + user)
            return redirect('home')
    else:
        form = BookForm()
    event = Anniversary.objects.get(id=id)
    return render(request,"firstapp/book.html", {'event': event})
def mbook(request, id):
    if request.method == 'POST':
        print(request.POST)
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data['username']
            messages.success(request ,'Account Created for' +"   " + user)
            return redirect('home')
    else:
        form = BookForm()
    event = Mothersday.objects.get(id=id)
    return render(request,"firstapp/book.html", {'event': event})


def bday(request):
    bday = Birthday.objects.all()
    dict={
        'bday' : bday,
        }
    return render(request,"firstapp/bday.html",dict)
def mom(request):
    mom = Mothersday.objects.all()
    dict={
        'mom' : mom,
        }
    return render(request,"firstapp/mother.html",dict)
def anni(request):
    anni = Anniversary.objects.all()
    dict={
        'anni' : anni
        }
    return render(request,"firstapp/anniversary.html",dict)


def profile(request, id , username):
    user = User.objects.get(id=id)
    book = Book.objects.filter(username= username)
    dict = {
        'user' : user,
        'book' : book,
    }
    return render(request, 'firstapp/profile.html', dict)

def update(request, id ):
    user = User.objects.get(id=id)
    form = UserCreationForm(request.POST, instance = user)
    if form.is_valid():
        form.save()
        return redirect("home")
    return render(request, 'firstapp/editprofile.html', {'user': user})

def destroy(request, id):
    book = Book.objects.get(id=id)
    book.delete()
    return redirect("/")

def reviewpage(request,id):
    if request.method == 'POST':
        print(request.POST)
        form = ReviewForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data['name']
            messages.success(request ,'Account Created for' +"   " + user)
            return redirect('home')
    else:
        form = ReviewForm()
        event = Book.objects.get(id=id)
        return render(request,"firstapp/review.html",{'event': event})
def reviews(request):
    rev = Review.objects.all()
    return render(request, "firstapp/reviewpages.html" ,{'rev' : rev})
