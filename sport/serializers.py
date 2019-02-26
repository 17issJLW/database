from rest_framework import serializers
from .models import *

class TeamSerializer(serializers.ModelSerializer):

    class Meta:
        model = Team
        fields = "__all__"

class RefereeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Referee
        fields = "__all__"