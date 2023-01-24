from django.forms import ModelForm
from .models import Book, Review,Genre
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms.widgets import NumberInput


class Book_Form(ModelForm):
    # genres=forms.ModelMultipleChoiceField(
    #     queryset=Genre.objects.all(),
    #     widget=forms.CheckboxSelectMultiple
    # )
    class Meta:
        model = Book
        fields = ['title', 'author', 'genres', 'pub_date_book', 'summary']
        labels = {
            'pub_date_book': 'Publication date',
            'summary': 'Book summary'
        }
        widgets = {
            'pub_date_book': NumberInput(attrs={'type': 'date'}),
            'genres': forms.CheckboxSelectMultiple
        }


CHOICES = (
    ("1", 1),
    ("2", 2),
    ("3", 3),
    ("4", 4),
    ("5", 5)
)


class Review_Form(ModelForm):
    stars = forms.ChoiceField(choices=CHOICES, initial=0, widget=forms.RadioSelect())

    class Meta:
        model = Review
        fields = ['title', 'content', 'stars']
        labels = {
            'title': 'Review Title',
            'content': 'Review',
            'stars': 'Rating',
        }
        widgets = {
        }


class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')