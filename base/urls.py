from django.shortcuts import render, redirect
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('book_reviews/<str:pk>/', views.book_selected, name='book_selected'),
    path('delete-book_review/<str:pk>/', views.delete_review, name='delete_review'),
    path('book_list/', views.book_list, name='book_list'),
    path('form_create_book/', views.add_book, name='add_book'),
    path('login/', views.login_to, name='login'),
    path('logout/', views.logout_my, name='logout'),
    path('add_review/<str:pk>/', views.add_review, name='add_review'),
    path('update_review/<str:pk>/',views.update_review,name='update_review'),

    path('register/', views.signup, name='register'),
    path('register/done', views.signup_complete, name='register_complete'),

    path('profile/', views.profile_my, name='profile'),

    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='base/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name="base/password_reset_confirm.html"), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='base/password_reset_complete.html'), name='password_reset_complete'),
    path("password_reset", views.password_reset_request, name="password_reset"),

    path('acc_active_email/(?P<uidb64>[0-9A-Za-z_\\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', views.activate
         , name='activate'),



]