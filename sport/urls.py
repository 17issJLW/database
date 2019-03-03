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

    path('leader_doctor/', LeaderAndDoctorView.as_view(), name="LeaderAndDoctorView"),
    path('leader_doctor/<int:people_id>/', LeaderAndDoctorView.as_view(), name="LeaderAndDoctorView"),
    path('coach/', CoachView.as_view(), name="CoachView"),
    path('coach/<int:people_id>/', CoachView.as_view(), name="CoachView"),
    path('team_update/', TeamUpdate.as_view(), name="TeamUpdate"),

    path('group/', GroupView.as_view(), name="GroupView"),
    path('group/<int:group_id>/', GroupView.as_view(), name="GroupView"),

    path('referee/', RefereeView.as_view(), name="RefereeView"),
    path('referee/<int:people_id>/', RefereeView.as_view(), name="RefereeView"),

]