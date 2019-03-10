from rest_framework import serializers
from .models import *

class TeamSerializer(serializers.ModelSerializer):


    class Meta:
        model = Team
        fields = "__all__"


class RefereeSerializer(serializers.ModelSerializer):
    team_name = serializers.ReadOnlyField(source="team.name")


    class Meta:
        model = Referee
        fields = "__all__"


class CompetitionSerializer(serializers.ModelSerializer):

    group =serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Competition
        fields = "__all__"

    def validate(self, attrs):
        if attrs['sex'] == "男" and attrs["name"] not in ["单杠","双杠","吊环","跳马","自由体操","鞍马","蹦床"]:
            raise serializers.ValidationError("比赛项目和性别不符")
        elif attrs['sex'] == "女" and attrs["name"] not in ["跳马","自由体操","平衡木","高低杠","蹦床"]:
            raise serializers.ValidationError("比赛项目和性别不符")

        return attrs

    def get_group(self,obj):
        group = obj.group_competition.all().values()
        return list(group)

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

    people = serializers.SerializerMethodField()


    class Meta:
        model = Group
        fields = "__all__"

    def get_people(self,obj):
        people = obj.sport_man.all().values()
        return list(people)

class SportManSerializer(serializers.ModelSerializer):

    team_name = serializers.ReadOnlyField(source="team.name")
    competition_group_list = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = SportMan
        fields = "__all__"

    def validate(self, attrs):
        if 7<= attrs['age'] <=8:
            attrs["age_group"] = "7-8"
        elif 9<= attrs['age'] <=10:
            attrs["age_group"] = "9-10"
        elif 11<= attrs['age'] <=12:
            attrs["age_group"] = "11-12"
        else:
            raise serializers.ValidationError("没有适合该年龄的比赛")
        return attrs

    def get_competition_group_list(self,obj):
        competition_group_list = obj.competition_group.all().values()
        return list(competition_group_list)


class SportManGroupSerializer(serializers.ModelSerializer):
    sport_man_name = serializers.ReadOnlyField(source="sid.name")
    sport_man_id = serializers.ReadOnlyField(source="sid.id_number")
    group_num = serializers.ReadOnlyField(source="gid.num")
    competition_name = serializers.ReadOnlyField(source="gid.competition.name")
    competition_sex = serializers.ReadOnlyField(source="gid.competition.sex")
    competition_age_group = serializers.ReadOnlyField(source="gid.competition.age_group")

    class Meta:
        model = SportManGroup
        fields = "__all__"

class RefereeGroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = RefereeGroup
        fields = "__all__"