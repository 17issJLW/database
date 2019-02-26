from django.contrib import admin
from django.urls import path,include
from .views import *
from django.views.static import serve
from database_project import settings

urlpatterns = [
    path('login/', UserLogin.as_view(), name="UserLogin"),

]