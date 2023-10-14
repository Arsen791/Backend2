
from django.contrib import admin
from django.urls import path, include
from user.views import user_login , register

urlpatterns = [
	path('login/', user_login),
	path('register/', register),
]
