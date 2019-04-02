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
    path('referee_update/', RefereeUpdate.as_view(), name="RefereeUpdate"),

    path('group/', GroupView.as_view(), name="GroupView"),
    path('group/<int:group_id>/', GroupView.as_view(), name="GroupView"),

    path('referee/', RefereeView.as_view(), name="RefereeView"),
    path('referee/<int:people_id>/', RefereeView.as_view(), name="RefereeView"),

    path('sport_man/', SportManView.as_view(), name="SportManView"),
    path('sport_man/<int:people_id>/', SportManView.as_view(), name="SportManView"),

    path('sign_up/', SignUpView.as_view(), name="SignUpView"),
    path('sign_up/<int:people_id>/', SignUpView.as_view(), name="SignUpView"),
    # path('sign_up/<int:sport_group_id>/', SignUpView.as_view(), name="SignUpView"),

    path('change_group/', ChangeGroupView.as_view(), name="ChangeGroupView"),
    path('change_referee_group/', ChangeRefereeGroupView.as_view(), name="ChangeRefereeGroupView"),
    path('change_referee_group/<int:people_id>/<int:group_id>/', ChangeRefereeGroupView.as_view(), name="ChangeRefereeGroupView"),
    path('start/', StartGame.as_view(), name="StartGame"),
    path('all_referee/', GetAllReferee.as_view(), name="GetAllReferee"),

    path('referee_grade/', GradeTheSport.as_view(), name="GradeTheSport"),
    path('get_sport_man/', GetSportMan.as_view(), name="GetSportMan"),
    path('get_all_sport_man/', GetAllSportMan.as_view(), name="GetAllSportMan"),
    path('grade_sport/', GradeTheSport.as_view(), name="GradeTheSport"),
    path('confirm_grade/',ConfirmGrade.as_view(), name='ConfirmGrade'),

    path('arrange/', Arrange.as_view(), name="Arrange"),

    path('rank/', Rank.as_view(), name="Rank"),

]