from django.contrib import admin
from django.urls import path,include


from .views import *
from rest_framework.routers import DefaultRouter
from django.views.static import serve
from database_project import settings




urlpatterns = [
    path('login/', UserLogin.as_view(), name="UserLogin"),

    path('team/', TeamView.as_view(), name="TeamView"),
    path('team/<int:team_id>/', TeamView.as_view(), name="TeamView"),
    path('competition/', CompetitionView.as_view(), name="CompetitionView"),
    path('competition/<int:competition_id>/', CompetitionView.as_view(), name="CompetitionView"),


]