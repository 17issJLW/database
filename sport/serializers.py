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

class CompetitionSerializer(serializers.ModelSerializer):

    class Meta:
        model = Competition
        fields = "__all__"

    def validate(self, attrs):
        if attrs['sex'] == "男" and attrs["name"] not in ["单杠","双杠","吊环","跳马","自由体操","鞍马","蹦床"]:
            raise serializers.ValidationError("比赛项目和性别不符")
        elif attrs['sex'] == "女" and attrs["name"] not in ["跳马","自由体操","平衡木","高低杠","蹦床"]:
            raise serializers.ValidationError("比赛项目和性别不符")

        return attrs

class LeaderAndDoctorSerializer(serializers.ModelSerializer):
    team = serializers.ReadOnlyField()

    class Meta:
        model = LeaderAndDoctor
        fields = "__all__"