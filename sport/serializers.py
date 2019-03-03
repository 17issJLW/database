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
    # team = serializers.ReadOnlyField()
    team_name = serializers.ReadOnlyField(source="team.name")

    class Meta:
        model = LeaderAndDoctor
        fields = "__all__"

class CoachSerializer(serializers.ModelSerializer):
    team_name = serializers.ReadOnlyField(source="team.name")

    class Meta:
        model = LeaderAndDoctor
        fields = "__all__"

class GroupSerializer(serializers.ModelSerializer):
    competition_name = serializers.ReadOnlyField(source="competition.name")
    competition_sex = serializers.ReadOnlyField(source="competition.sex")
    competition_age_group = serializers.ReadOnlyField(source="competition.age_group")

    class Meta:
        model = Group
        fields = "__all__"