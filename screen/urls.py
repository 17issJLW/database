
from django.urls import path,include

from screen import views




urlpatterns = [
    path('', views.index, name="index"),

]