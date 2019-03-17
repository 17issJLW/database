from lib.rest_framework.exceptions import *
from rest_framework.views import APIView, status,Response
from lib.rest_framework.util import *
from lib.rest_framework.permissions import check_token,check_team_token,check_referee_token
from rest_framework.pagination import PageNumberPagination


from .models import *
from .serializers import *
# Create your views here.

class Pagination(PageNumberPagination):
    """
    配置分页规则
    """
    page_size = 20                          #每页显示数目
    page_size_query_param = 'size'          #控制每页显示数目的参数
    page_query_param = 'page'               #获得页数的参数
    max_page_size = 500                     #每页最大显示数目

class UserLogin(APIView):
    """
    登录视图
    """
    @check_token
    def get(self,request):
        type = request.META.get("REMOTE_USER").get("type")
        username = request.META.get("REMOTE_USER").get("username")
        if type == "team":
            queryset = Team.objects.filter(username=username).first()
            serializer = TeamSerializer(queryset)
            return Response(serializer.data)

        if type == "referee":
            queryset = Referee.objects.filter(username=username).first()
            serializer = RefereeSerializer(queryset)
            return Response(serializer.data)

        if type == "admin":
            return Response({"username":"admin","type":"admin"})


    def post(self,request):
        request_data = request.data
        username = request_data.get("username")
        password = request_data.get("password")
        account_type = request_data.get("type")
        if username is None or password is None or account_type is None:
            raise BadRequest
        if account_type == "admin":
            if username == "admin" and password == "admin":
                payload = {"type":"admin","username":"admin","name":"管理员"}
                token = create_jwt(payload)
                return Response({"token":token,"username":"admin","name":"管理员"},status=status.HTTP_200_OK)
            else:
                raise PasswordError

        if account_type == "team":
            team = Team.objects.filter(username=username,password=password).first()
            if team:
                payload = {"type":"team","username":username,"name":team.name}
                token = create_jwt(payload)
                return Response({"token": token, "username": username, "name": team.name}, status=status.HTTP_200_OK)
            else:
                raise PasswordError

        if account_type == "referee":
            referee = Referee.objects.filter(username=username,password=password).first()
            if referee:
                payload = {"type": account_type, "username": username, "name": referee.name}
                token = create_jwt(payload)
                return Response({"token": token, "username": username, "name": referee.name}, status=status.HTTP_200_OK)
            else:
                raise PasswordError


class TeamView(APIView):

    @check_token
    def get(self,request):
        type = request.META.get("REMOTE_USER").get("type")
        if type != "admin":
            raise PermissionDeny

        queryset = Team.objects.all()
        page = Pagination()
        result = page.paginate_queryset(queryset=queryset,request=request,view=self)
        serializer = TeamSerializer(result,many=True)
        return page.get_paginated_response(serializer.data)

    @check_token
    def post(self,request):
        type = request.META.get("REMOTE_USER").get("type")
        if type != "admin":
            raise PermissionDeny
        serializer = TeamSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
            team = Team.objects.create(
                username=data.get("username"),
                password=data.get("password"),
                name = data.get("name"),
            )
            return Response({"username":team.username,"password":team.password,"name":team.name},status=status.HTTP_201_CREATED)
        else:
            raise BadRequest

    @check_token
    def put(self,request,team_id):
        type = request.META.get("REMOTE_USER").get("type")
        if type != "admin":
            raise PermissionDeny
        team = Team.objects.filter(pk=team_id).first()
        if team:
            serializer = TeamSerializer(team,data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            raise TeamNotFound

    @check_token
    def delete(self, request,team_id):
        type = request.META.get("REMOTE_USER").get("type")
        if type != "admin":
            raise PermissionDeny
        team = Team.objects.filter(pk=team_id).first()
        if team:
            serializer = TeamSerializer(team)
            team.delete()
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            raise TeamNotFound

class TeamUpdate(APIView):

    @check_team_token
    def get(self,request):
        username = request.META.get("REMOTE_USER").get("username")
        queryset = Team.objects.filter(username=username).first()
        serializer = TeamSerializer(queryset)
        return Response(serializer.data)

    @check_team_token
    def post(self,request):
        username = request.META.get("REMOTE_USER").get("username")
        team = Team.objects.filter(username=username).first()
        request_data = request.data
        if team:
            password = request_data.get("password")
            name = request_data.get("name")
            file = request_data.get("file")
            print(password,name,file)
            if password and name and file:
                team.password = password
                team.name = name
                team.file = file
                team.save()
                # serializer = TeamSerializer(team)
                return Response({"ok"}, status=status.HTTP_200_OK)
            elif password and name:
                team.password = password
                team.name = name
                team.save()
                # serializer = TeamSerializer(team)
                return Response({"ok"}, status=status.HTTP_200_OK)
            else:
                raise BadRequest
        else:
            raise TeamNotFound



class CompetitionView(APIView):

    @check_token
    def get(self,request):
        queryset = Competition.objects.all()
        page = Pagination()
        result = page.paginate_queryset(queryset=queryset,request=request,view=self)
        serializer = CompetitionSerializer(result,many=True)
        return page.get_paginated_response(serializer.data)

    @check_token
    def post(self,request):
        type = request.META.get("REMOTE_USER").get("type")
        if type != "admin":
            raise PermissionDeny
        serializer = CompetitionSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
            competition = Competition.objects.create(
                name=data.get("name"),
                age_group=data.get("age_group"),
                sex=data.get("sex")
            )
            group = Group.objects.get_or_create(num=0, competition=competition,level="初赛")
            return Response(data,status=status.HTTP_201_CREATED)
        else:
            raise BadRequest

    @check_token
    def put(self,request,competition_id):
        type = request.META.get("REMOTE_USER").get("type")
        if type != "admin":
            raise PermissionDeny
        competition = Competition.objects.filter(pk=competition_id).first()
        if competition:
            serializer = CompetitionSerializer(competition,data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            raise NotFound

    @check_token
    def delete(self, request,competition_id):
        type = request.META.get("REMOTE_USER").get("type")
        if type != "admin":
            raise PermissionDeny
        competition = Competition.objects.filter(pk=competition_id).first()
        if competition:
            competition.delete()
            return Response({"ok"},status=status.HTTP_200_OK)
        else:
            raise NotFound


class GroupView(APIView):

    # @check_token
    def get(self,request):
        # type = request.META.get("REMOTE_USER").get("type")
        # if type != "admin":
        #     raise PermissionDeny
        queryset = Group.objects.select_related("competition").all()
        page = Pagination()
        result = page.paginate_queryset(queryset=queryset, request=request, view=self)
        serializer = GroupSerializer(queryset,many=True)
        return page.get_paginated_response(serializer.data)

    @check_token
    def post(self,request):
        type = request.META.get("REMOTE_USER").get("type")
        if type != "admin":
            raise PermissionDeny
        serializer = GroupSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            raise BadRequest

    @check_token
    def delete(self,request,group_id):
        type = request.META.get("REMOTE_USER").get("type")
        if type != "admin":
            raise PermissionDeny
        group = Group.objects.filter(pk=group_id).first()
        if group:
            serializer = GroupSerializer(group)
            group.delete()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            raise NotFound







class LeaderAndDoctorView(APIView):

    @check_team_token
    def get(self,request):
        username = request.META.get("REMOTE_USER").get("username")
        queryset = LeaderAndDoctor.objects.filter(team__username=username)
        page = Pagination()
        result = page.paginate_queryset(queryset=queryset, request=request, view=self)
        serializer = LeaderAndDoctorSerializer(result, many=True)
        return page.get_paginated_response(serializer.data)

    @check_team_token
    def post(self,request):
        username = request.META.get("REMOTE_USER").get("username")
        try:
            team = Team.objects.get(username=username)
        except:
            raise NotFound
        serializer = LeaderAndDoctorSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
            people = LeaderAndDoctor.objects.create(
                name=data.get("name"),
                id_number=data.get("id_number"),
                phone=data.get("phone"),
                place=data.get("place"),
                team=team
            )
            serializer = LeaderAndDoctorSerializer(people)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            raise BadRequest

    @check_team_token
    def put(self, request, people_id):
        username = request.META.get("REMOTE_USER").get("username")
        people = LeaderAndDoctor.objects.filter(pk=people_id,team__username=username).first()
        if people:
            serializer = LeaderAndDoctorSerializer(people, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            raise NotFound

    @check_token
    def delete(self, request, people_id):
        username = request.META.get("REMOTE_USER").get("username")
        people = LeaderAndDoctor.objects.filter(pk=people_id, team__username=username).first()
        if people:
            serializer = LeaderAndDoctorSerializer(people)
            people.delete()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            raise NotFound


class CoachView(APIView):

    @check_team_token
    def get(self,request):
        username = request.META.get("REMOTE_USER").get("username")
        queryset = Coach.objects.filter(team__username=username)
        page = Pagination()
        result = page.paginate_queryset(queryset=queryset, request=request, view=self)
        serializer = CoachSerializer(result, many=True)
        return page.get_paginated_response(serializer.data)

    @check_team_token
    def post(self,request):
        username = request.META.get("REMOTE_USER").get("username")
        try:
            team = Team.objects.get(username=username)
        except:
            raise NotFound
        serializer = CoachSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
            coach = Coach.objects.create(
                name=data.get("name"),
                id_number=data.get("id_number"),
                phone=data.get("phone"),
                team=team
            )
            serializer = CoachSerializer(coach)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            raise BadRequest

    @check_team_token
    def put(self, request, people_id):
        username = request.META.get("REMOTE_USER").get("username")
        coach = Coach.objects.filter(pk=people_id).first()
        if coach:
            serializer = CoachSerializer(coach, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            raise NotFound

    @check_token
    def delete(self, request, people_id):
        username = request.META.get("REMOTE_USER").get("username")
        coach = Coach.objects.filter(pk=people_id, team__username=username).first()
        if coach:
            serializer = CoachSerializer(coach)
            coach.delete()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            raise NotFound

class RefereeView(APIView):

    @check_team_token
    def get(self, request):
        username = request.META.get("REMOTE_USER").get("username")
        queryset = Referee.objects.filter(team__username=username)
        page = Pagination()
        result = page.paginate_queryset(queryset=queryset, request=request, view=self)
        serializer = RefereeSerializer(result, many=True)
        return page.get_paginated_response(serializer.data)

    @check_team_token
    def post(self, request):
        username = request.META.get("REMOTE_USER").get("username")
        try:
            team = Team.objects.get(username=username)
        except:
            raise NotFound
        serializer = RefereeSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
            referee = Referee.objects.create(
                username=data.get("username"),
                password=data.get("password"),
                name=data.get("name"),
                id_number=data.get("id_number"),
                phone=data.get("phone"),
                team=team
            )
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            raise BadRequest

    @check_team_token
    def put(self, request, people_id):
        username = request.META.get("REMOTE_USER").get("username")
        referee = Referee.objects.filter(pk=people_id,team__username=username).first()
        if referee:
            serializer = RefereeSerializer(referee, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            raise NotFound

    @check_team_token
    def delete(self, request, people_id):
        username = request.META.get("REMOTE_USER").get("username")
        referee = Referee.objects.filter(pk=people_id, team__username=username).first()
        if referee:
            serializer = RefereeSerializer(referee)
            referee.delete()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            raise NotFound

class SportManView(APIView):
    """

    name = models.CharField(verbose_name="姓名",max_length=32,db_index=True)
    id_number = models.CharField(verbose_name="身份证号码", max_length=18, default="", unique=True)
    age = models.IntegerField(verbose_name="年龄", blank=True, null=True)
    sex = models.CharField(verbose_name="性别", max_length=32, default="男", choices=SEX)
    age_group = models.CharField(verbose_name="组别",default="7-8岁",choices=AGEGROUP,max_length=32)
    grade = models.FloatField(verbose_name="文化分数", blank=True, null=True)
    team = models.ForeignKey("Team", verbose_name="所属代表队",blank=True,null=True,on_delete=models.SET_NULL,related_name='sport_man_team')
    competition_group = models.ManyToManyField("Group", verbose_name="报名分组", through='SportManGrou
    """

    @check_team_token
    def get(self,request):
        username = request.META.get("REMOTE_USER").get("username")
        queryset = SportMan.objects.filter(team__username=username)
        page = Pagination()
        result = page.paginate_queryset(queryset=queryset, request=request, view=self)
        serializer = SportManSerializer(result, many=True)
        return page.get_paginated_response(serializer.data)

    @check_team_token
    def post(self,request):
        username = request.META.get("REMOTE_USER").get("username")
        try:
            team = Team.objects.get(username=username)
        except:
            raise NotFound
        serializer = SportManSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            data = serializer.validated_data
            sport_man = SportMan.objects.create(
                name=data.get("name"),
                id_number=data.get("id_number"),
                age=data.get("age"),
                age_group=data.get("age_group"),
                sex=data.get("sex"),
                team=team
            )
            return Response(data,status=status.HTTP_200_OK)
        else:
            raise BadRequest

    @check_team_token
    def put(self,request,people_id):
        username = request.META.get("REMOTE_USER").get("username")
        try:
            team = Team.objects.get(username=username)
        except:
            raise NotFound

        sport_man = SportMan.objects.filter(pk=people_id, team__username=username).first()
        if sport_man:
            serializer = SportManSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            data = serializer.validated_data
            sport_man = SportMan.objects.create(
                name=data.get("name"),
                id_number=data.get("id_number"),
                age=data.get("age"),
                sex=data.get("sex"),
                age_group=data.get("age_group")
            )
            serializer = SportManSerializer(sport_man)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            raise NotFound

    @check_team_token
    def delete(self, request, people_id):
        username = request.META.get("REMOTE_USER").get("username")
        sport_man = SportMan.objects.filter(pk=people_id, team__username=username).first()
        if sport_man:
            serializer = SportManSerializer(sport_man)
            sport_man.delete()
            return Response({"OK"}, status=status.HTTP_200_OK)
        else:
            raise NotFound


class SignUpView(APIView):

    @check_team_token
    def get(self,request):
        username = request.META.get("REMOTE_USER").get("username")
        queryset = SportManGroup.objects.filter(sid__team__username=username).order_by("sid__id")
        page = Pagination()
        result = page.paginate_queryset(queryset=queryset, request=request, view=self)
        serializer = SportManGroupSerializer(result, many=True)
        return page.get_paginated_response(serializer.data)


    @check_team_token
    def put(self,request,people_id):
        username = request.META.get("REMOTE_USER").get("username")
        request_data = request.data
        sport_man = SportMan.objects.filter(pk=people_id,team__username=username).first()
        competition = Competition.objects.filter(pk=request_data.get("competition")).first()
        if not sport_man or not competition:
            raise NotFound
        if sport_man.sex == competition.sex and sport_man.age_group == competition.age_group:
            if SportManGroup.objects.filter(sid__team__username=username,gid__competition__id=request_data.get("competition")).count() >= 6:
                raise TooManyPeople
            group,success = Group.objects.get_or_create(num=0, competition=competition, level="初赛")
            sport_man_group = SportManGroup.objects.create(sid=sport_man, gid=group)
            serializer = SportManGroupSerializer(sport_man_group)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            raise NotMatch


    @check_team_token
    def delete(self,request,people_id,competition_id):
        username = request.META.get("REMOTE_USER").get("username")
        sport_man = SportMan.objects.filter(pk=people_id, team__username=username).first()
        if not sport_man:
            raise NotFound
        sport_man_group = SportManGroup.objects.filter(sid__id=people_id, gid__competition__id=competition_id).first()
        if sport_man_group:
            sport_man_group.delete()
        else:
            raise NotFound

class GetSportMan(APIView):

    @check_token
    def get(self,request):
        queryset = SportManGroup.objects.filter(sid__isnull=False)
        serializer = SportManGroupSerializer(queryset,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)


class RefereeUpdate(APIView):

    @check_referee_token
    def get(self,request):
        username = request.META.get("REMOTE_USER").get("username")
        queryset = Referee.objects.filter(username=username).first()
        serializer = RefereeSerializer(queryset)
        return Response(serializer.data)

    @check_referee_token
    def post(self, request):
        username = request.META.get("REMOTE_USER").get("username")
        referee = Referee.objects.filter(username=username).first()
        if referee:
            serializer = RefereeSerializer(referee, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(request.data,status=status.HTTP_200_OK)
        else:
            raise NotFound

class ChangeGroupView(APIView):

    @check_token
    def get(self,request,group_id):
        group = Group.objects.filter(pk=group_id).first()
        serializer = GroupSerializer(group)
        return Response(serializer.data,status=status.HTTP_200_OK)


    @check_token
    def post(self, request):
        type = request.META.get("REMOTE_USER").get("type")
        if type != "admin":
            raise PermissionDeny
        request_data = request.data
        people = request_data.get("people_list")
        group_id = request_data.get("group")
        competiton_id = request_data.get("competition")
        group = Group.objects.filter(pk=group_id).first()
        print("1")
        print(people, group_id, competiton_id)
        if not people or not group:
            raise NotFound
        print("hhh")
        print(people,group_id,competiton_id)
        try:
            for i in people:
                sport_man_group = SportManGroup.objects.filter(sid__id=i, gid__competition__id=competiton_id).first()
                if sport_man_group:
                    sport_man_group.gid = group
                    sport_man_group.save()
                else:
                    return Response({"Not Found"}, status=status.HTTP_404_NOT_FOUND)
        except:
            raise UnknowError

        return Response({"ok"}, status=status.HTTP_200_OK)

class ChangeRefereeGroupView(APIView):

    @check_token
    def get(self, request):
        group = RefereeGroup.objects.all()
        serializer = RefereeGroupSerializer(group,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @check_token
    def post(self,request):
        type = request.META.get("REMOTE_USER").get("type")
        if type != "admin":
            raise PermissionDeny
        request_data = request.data
        people = request_data.get("people_list")
        group_id = request_data.get("group")
        group = Group.objects.filter(pk=group_id).first()
        print(people, group_id)
        if not people or not group:
            raise NotFound
        # try:
        for i in people:
            referee_group = RefereeGroup.objects.filter(group__id=group_id, referee__id=i).first()
            if referee_group:
                pass
            else:
                referee = Referee.objects.filter(pk=i).first()
                referee_group = RefereeGroup.objects.create(group=group,referee=referee)

        return Response({"ok"},status=status.HTTP_200_OK)
        # except:
        #     raise UnknowError

    @check_token
    def delete(self,request,people_id,group_id):
        type = request.META.get("REMOTE_USER").get("type")
        if type != "admin":
            raise PermissionDeny
        referee_group = RefereeGroup.objects.filter(group__id=group_id, referee__id=people_id)
        referee_group.delete()
        return Response({"ok"},status=status.HTTP_200_OK)


class GetAllReferee(APIView):

    @check_token
    def get(self, request):
        referee = Referee.objects.all()
        serializer = RefereeSerializer(referee,many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class StartGame(APIView):

    @check_token
    def get(self,request):
        queryset = Group.objects.all()
        serializer = GroupSerializer(queryset,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

    @check_token
    def post(self,request):
        type = request.META.get("REMOTE_USER").get("type")
        if type != "admin":
            raise PermissionDeny
        group_id = request.data.get("group")
        group = Group.objects.filter(pk=group_id).first()
        if group:
            if group.status != "未开始":
                raise StatusError
            group.status = "待打分"
            group.save()
            return Response({"message":group_id}, status=status.HTTP_200_OK)
        else:
            raise NotFound


class GradeTheSport(APIView):

    @check_referee_token
    def get(self,request):
        username = request.META.get("REMOTE_USER").get("username")
        referee = Referee.objects.filter(username=username).first()
        group_list = list(referee.group.filter(status="待打分").values("id"))
        group_id = []
        for group in group_list:
            group_id.append(group.get("id"))
        group = Group.objects.filter(pk__in=group_id)
        serializer = GroupSerializer(group, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


    @check_referee_token
    def post(self, request):
        username = request.META.get("REMOTE_USER").get("username")
        referee = Referee.objects.filter(username=username).first()
        data = request.data
        if data["group"] and data["sport_man"] and data["grade"]:
            group = Group.objects.filter(pk=data["group"]).first()
            sport_man = SportMan.objects.filter(pk=data["sport_man"]).first()
            if not group or not sport_man:
                raise NotFound

            score = Score.objects.filter(
                referee__id=referee.id,
                group__id=data["group"],
                sport_man__id=data["sport_man"],
            ).first()
            if score:
                score.grade = data["grade"]
                score.save()
            else:
                Score.objects.create(
                    referee=referee,
                    group=group,
                    sport_man=sport_man,
                    score=data["score"]
                )
            count = Score.objects.filter(group__id=data["group"]).count()
            if count >= 5:
                group.status = "待审核"
                group.save()
            return Response({"ok"}, status=status.HTTP_200_OK)
        else:
            raise BadRequest

class CheckGrade(APIView):

    @check_referee_token
    def get(self,request, group_id):
        score = Score.objects.filter(group__id=group_id)
        pass


class ConfirmGrade(APIView):

    @check_referee_token
    def get(self,request):
        username = request.META.get("REMOTE_USER").get("username")
        group_list = RefereeGroup.objects.filter(referee__username=username,is_leader=True)
        if group_list:
            group_id = []
            for i in group_list:
                group_id.append(i.group)
            pass
        else:
            return Response({"message":"您不是小组总裁判"})













