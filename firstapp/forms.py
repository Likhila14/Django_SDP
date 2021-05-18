from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Book , Review ,Bill



class CreateUserForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')
    class Meta:
        model = User
        fields = ['first_name','username','email','password1','password2']
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = "__all__"

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = "__all__"
class BillForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = "__all__"
