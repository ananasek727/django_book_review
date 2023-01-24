from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.shortcuts import render
from .models import Book, Review, Genre
from .forms import Book_Form, Review_Form
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Sign Up Form
from django.contrib.auth import login, authenticate, logout
from .forms import SignupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from BookReview.token import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm
from django.db.models.query_utils import Q
from django.contrib.auth.tokens import default_token_generator




# My function

def unique_book(title):
    all_books = Book.objects.all()
    for t in all_books:
        if str(t.title).lower() == str(title).lower():
            return False
    return True


# view function

def home(request):
    return render(request, 'base/main.html')


def book_selected(request, pk):
    book = Book.objects.get(id=int(pk))
    reviews = Review.objects.filter(book_id=int(pk))
    return render(request, 'base/book_reviews.html', {"reviews": reviews, "book": book})


def book_list(request):
    query = ''
    if request.GET.get('q') is not None:
        query = request.GET.get('q')
        book = Book.objects.filter(title=query)
    elif request.GET.get('g') is not None:
        # genre
        query = request.GET.get('g')
        book = Book.objects.filter(genres__name=query)
    else:
        book = Book.objects.all()

    genre = Genre.objects.all()
    return render(request, 'base/book_list.html', context={'books': book, 'genres': genre})


@login_required(login_url='login')
def add_book(request):
    form = Book_Form()
    if request.method == 'POST':
        if not unique_book(request.POST.get('title')):
            return redirect('book_list')
        form = Book_Form(request.POST)
        if form.is_valid():
            missing_fields = form.save(commit=False)
            missing_fields.numbers_of_review = 0
            missing_fields.stars = 0
            missing_fields.save()
            return redirect('book_list')
    context = {'form': form}
    return render(request, 'base/form_add_book.html', context=context)


@login_required(login_url='login')
def add_review(request, pk):
    form_review = Review_Form()
    if request.method == 'POST':
        form_review = Review_Form(request.POST)
        if form_review.is_valid():
            book = Book.objects.get(id=int(pk))
            missing_fields = form_review.save(commit=False)
            missing_fields.book = book
            missing_fields.user = request.user
            missing_fields.save()
            book.numbers_of_review = book.numbers_of_review + 1
            book.stars = (book.stars + int(form_review.cleaned_data['stars']))/book.numbers_of_review
            book.save()
            return redirect('book_list')
    context = {'form': form_review}
    return render(request, 'base/form_add_review.html', context=context)


@login_required(login_url='login')
def update_review(request,pk):
    review = Review.objects.get(id=int(pk))
    form = Review_Form(instance=review)
    if request.method =='POST':
        form = Review_Form(request.POST, instance=review)
        if form.is_valid():
            form.save()
        return redirect('book_list')
    context = {'form':form}
    return render(request, 'base/form_add_review.html',context=context)


@login_required(login_url='login')
def delete_review(request, pk):
    review = Review.objects.get(id=int(pk))
    if request.method == 'POST':
        # if user clicked Yes then the form was sent
        review.delete()
        return redirect('book_list')
    return render(request, 'base/delete_review.html', context={'title': review.title})


def login_to(request):
    page = 'login'
    if request.method == 'POST':
        user_name = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=user_name)
        except:
            messages.error(request, "Wrong username or password")
        user_authenticate = authenticate(request, username=user_name, password=password)
        if user_authenticate is not None:
            login(request, user_authenticate)
            return redirect('book_list')
        else:
            messages.error(request, "Wrong username or password !!!")
    context = {'page': page}
    return render(request, 'base/login_or_register.html', context)


@login_required(login_url='login')
def logout_my(request):
    logout(request)
    return redirect('book_list')


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            # save form in the memory not in database
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            # to get the domain of the current site
            current_site = get_current_site(request)
            mail_subject = 'Activation link has been sent to your email id'
            message = render_to_string('base/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email]
            )
            email.send()
            return redirect('register_complete')
    else:
        form = SignupForm()
    return render(request, 'base/signup.html', {'form': form})


def signup_complete(request):
    return render(request, 'base/signup_complete.html')


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Thank you for your email confirmation. Now you can log in to your account.')
    else:
        return HttpResponse('Activation link is invalid!')


@login_required(login_url='login')
def profile_my(request):
    reviews = Review.objects.filter(user=request.user)

    context = {'reviews': reviews}
    return render(request, 'base/profile.html', context=context)


def password_reset_request(request):

    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data.get('email')


            associated_users = User.objects.filter(email=data)
            for user in associated_users:

                    mail_subject = "Password Reset Requested"
                    current_site = get_current_site(request)
                    message = render_to_string('base/acc_reset_password.html', {
                        "email": user.email,
                        'domain': current_site,
                        'site_name': 'Website',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    })
                    to_email = password_reset_form.cleaned_data.get('email')
                    email = EmailMessage(
                        mail_subject, message, to=[to_email]
                    )
                    email.send()
                    return redirect("password_reset/done/")
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="base/password_reset.html",
                  context={"password_reset_form": password_reset_form})
