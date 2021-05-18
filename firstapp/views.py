
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
from django.contrib.auth.decorators import login_required 
from django.contrib.sites.shortcuts import get_current_site 
from django.core.mail import EmailMessage 
from django.contrib.auth import login, authenticate 
from django.shortcuts  import render
from django.http import HttpResponse,JsonResponse
from django.shortcuts import render, redirect 
from django.template.loader import render_to_string 
from django.utils.encoding import force_bytes, force_text 
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode 
from .forms import CreateUserForm, UserCreationForm , BookForm , ReviewForm 
from django.contrib import messages 
from .models import Mothersday, Register,Birthday,Anniversary
from django.db.models import Q 
from django.contrib.auth import authenticate, login as log_in, logout, login 
from django.contrib.auth.models import User 
from .models import Book,Review 
from .tokens import account_activation_token


def register(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid(): 
            user = form.save(commit = False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            message = render_to_string('acc_active_email.html', {
            'user':user, 'domain':current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user),})
            mail_subject = 'Activate your account.'
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(mail_subject, message, to=[to_email])
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration.')
    else:
        form = CreateUserForm()
    return render(request, 'firstapp/register.html', {'form': form})


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

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        log_in(request, user)
        return render(request,"firstapp/home.html")
                #return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')



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

def service(request):
    bday = Birthday.objects.all()[:4]
    anni = Anniversary.objects.all()[:4]
    mom = Mothersday.objects.all()[:4]
    dict={
        'bday' : bday,
        'anni' : anni,
        'mom' : mom
    }
    return render(request,"firstapp/services.html",dict)

def contactus(request):
    return render(request, "firstapp/contact.html")
def aboutus(request):
    return render(request, "firstapp/aboutus.html")

def logoutUser(request):
    logout(request)
    messages.success(request ,'Logged Out Successfully')
    return redirect('login')



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


def destroy(request, id):
    book = Book.objects.get(id=id)
    book.delete()
    return redirect("/")



def reviews(request):
    rev = Review.objects.all()
    return render(request, "firstapp/reviewpages.html" ,{'rev' : rev})

@login_required(login_url ='login' )    
def bill(request,username):
    book = Book.objects.filter(username= username)
    fprice =[]
    for i in range(0,len(book)):
        fprice[i] = (((book[i].nop)*80)*(book[i].noti))+book[i].price
        if(book[i].loc =='yes'):
            fprice[i] = fprice[i] + 30000
        if(book[i].cam =='yes'):
            fprice[i] = fprice[i] + 20000
        if(book[i].ent =='yes'):
            fprice[i] = fprice[i] + 10000
    dict = {
        'fprice' : fprice,
         'book' : book
    }

    return render(request, "firstapp/bill.html", dict)

@login_required(login_url ='login' )
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

@login_required(login_url ='login' )
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

@login_required(login_url ='login' )
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

    

@login_required(login_url ='login' )
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

@login_required(login_url ='login' )
def profile(request, id , username):
    user = User.objects.get(id=id)
    book = Book.objects.filter(username= username)
    dict = {
        'user' : user,
        'book' : book,
    }
    return render(request, 'firstapp/profile.html', dict)

@login_required(login_url ='login' )
def update(request, id ):
    user = User.objects.get(id=id)
    form = UserCreationForm(request.POST, instance = user)
    if form.is_valid():
        form.save()
        return redirect("home")
    return render(request, 'firstapp/editprofile.html', {'user': user})
