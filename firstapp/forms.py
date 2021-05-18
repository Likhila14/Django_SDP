from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Book



class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name','username','email','password1','password2']
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = "__all__"