from lib.rest_framework.exceptions import *
from rest_framework.views import APIView, status,Response
from lib.rest_framework.util import *
from lib.rest_framework.permissions import check_token,check_team_token,check_referee_token
from rest_framework.pagination import PageNumberPagination
from django.db.models import Avg,Min,Max,Sum,Q


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
                id_number=str(data.get("id_number")),
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
    def put(self,request, people_id):
        username = request.META.get("REMOTE_USER").get("username")
        request_data = request.data
        sport_man = SportMan.objects.filter(pk=people_id, team__username=username).first()
        competition = Competition.objects.filter(pk=request_data.get("competition")).first()
        if not sport_man or not competition:
            raise NotFound
        if sport_man.sex == competition.sex and sport_man.age_group == competition.age_group:
            if SportManGroup.objects.filter(sid__team__username=username, gid__competition__age_group=sport_man.age_group, gid__competition__sex=sport_man.sex).count() >= 6:
                raise TooManyPeople
            group,success = Group.objects.get_or_create(num=0, competition=competition, level="初赛")
            sport_man_group = SportManGroup.objects.filter(sid=sport_man, gid=group).first()
            if sport_man_group:
                raise Repetition
            else:
                sport_man_group = SportManGroup.objects.create(sid=sport_man, gid=group)
            serializer = SportManGroupSerializer(sport_man_group)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            raise NotMatch


    @check_team_token
    def delete(self,request,people_id):
        username = request.META.get("REMOTE_USER").get("username")
        sport_man_group = SportManGroup.objects.filter(pk=people_id, sid__team__username=username).first()
        if sport_man_group:
            sport_man_group.delete()
            return Response({"ok"},status=status.HTTP_200_OK)
        else:
            raise NotFound

class GetSportMan(APIView):

    @check_token
    def get(self,request):
        queryset = SportManGroup.objects.filter(sid__isnull=False)
        serializer = SportManGroupSerializer(queryset,many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class GetAllSportMan(APIView):

    @check_token
    def get(self,request):
        queryset = SportMan.objects.filter(team__isnull=False).order_by("number")
        page = Pagination()
        result = page.paginate_queryset(queryset=queryset, request=request, view=self)
        serializer = SportManSerializer(result, many=True)
        return page.get_paginated_response(serializer.data)


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
    def put(self,request,people_id, group_id):
        type = request.META.get("REMOTE_USER").get("type")
        if type != "admin":
            raise PermissionDeny
        referee_group = RefereeGroup.objects.filter(referee__id=people_id,group__id=group_id).first()
        leader = RefereeGroup.objects.filter(group__id=group_id,is_leader=True)
        if leader:
            leader.update(is_leader=False)
        if referee_group:
            referee_group.is_leader = True
            referee_group.save()
            return Response({"message":"ok"}, status=status.HTTP_200_OK)
        else:
            raise NotFound



    @check_token
    def delete(self,request,people_id,group_id):
        type = request.META.get("REMOTE_USER").get("type")
        if type != "admin":
            raise PermissionDeny
        referee_group = RefereeGroup.objects.filter(group__id=group_id, referee__id=people_id)
        referee_group.delete()
        return Response({"ok"}, status=status.HTTP_200_OK)


class GetAllReferee(APIView):

    @check_token
    def get(self, request):
        referee = Referee.objects.all()
        serializer = AllRefereeSerializer(referee, many=True)
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
            if RefereeGroup.objects.filter(group__id=group_id).count() < 3:
                raise TooLessReferee
            if not RefereeGroup.objects.filter(group__id=group_id,is_leader=True):
                raise NoRefereeLeader
            group.status = "待打分"
            group.save()
            return Response({"message":group_id}, status=status.HTTP_200_OK)
        else:
            raise NotFound

class Arrange(APIView):

    @check_token
    def post(self, request):
        type = request.META.get("REMOTE_USER").get("type")
        if type != "admin":
            raise PermissionDeny
        host = request.data.get("host")
        if not host:
            raise BadRequest
        man = 1
        woman = 0
        sport_man = SportMan.objects.filter(team__isnull=False)
        for person in sport_man:
            if person.team.id == host:
                continue
            if person.sex == "男":
                person.number = man
                person.save()
                man = man + 2
            elif person.sex == "女":
                person.number = woman
                person.save()
                woman = woman + 2
        host_people = SportMan.objects.filter(team__id=host)
        for person in host_people:
            if person.sex == "男":
                person.number = man
                person.save()
                man = man + 2
            elif person.sex == "女":
                person.number = woman
                person.save()
                woman = woman + 2

        return Response({"message":"ok"},status=status.HTTP_200_OK)




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
                score.status = "待审核"
                score.save()
            else:
                Score.objects.create(
                    referee=referee,
                    group=group,
                    sport_man=sport_man,
                    grade=float(data["grade"])
                )
            count = Score.objects.filter(group__id=data["group"]).count()
            people_count = SportManGroup.objects.filter(gid__id=data["group"]).count()
            if count >= people_count:
                group.status = "待审核"
                group.save()
            return Response({"ok"}, status=status.HTTP_200_OK)
        else:
            raise BadRequest

class SportManGrade(APIView):

    @check_referee_token
    def get(self,request, group_id):
        username = request.META.get("REMOTE_USER").get("username")
        referee = Referee.objects.filter(username=username).first()
        referee_id = referee.id
        sport_man = SportMan.objects.raw("""select sport_sportman.id,name,id_number,age,sex,number,table2.status,table2.grade,team_id
                                            from sport_sportmangroup
                                            left join(
                                              select * from sport_score where referee_id=%s and group_id=%s
                                            ) as table2 on sport_sportmangroup.sid_id = table2.sport_man_id 
                                            left join sport_sportman on sport_sportmangroup.sid_id = sport_sportman.id
                                            where sport_sportmangroup.gid_id=%s
                                            order by number
                                            """, [referee_id, group_id, group_id])
        serializer = SportManGradeSerializer(sport_man, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class ConfirmGrade(APIView):

    @check_referee_token
    def get(self,request):
        username = request.META.get("REMOTE_USER").get("username")
        group_list = RefereeGroup.objects.filter(referee__username=username, is_leader=True, group__status="待审核")
        if group_list:
            group_id = []
            for i in group_list:
                group_id.append(i.group.id)
            score_list = Score.objects.filter(group__id__in=group_id).order_by("group")
            serializer = ScoreSerializer(score_list,many=True)
            data = serializer.data
            result = {}
            group_list_id = []
            sport_man = []
            # for i in data:
            #     group_list_id.append(i["group_id"])
                # for j in data:
                #     if j["group_id"] == i["group_id"]:
                #         for k in data:
                #
                #         temp.append(j)
                #
                # result[i["group_id"]] = temp
                # temp = []
            for i in data:
                group_list_id.append(i["group_id"])
            group_list_id = list(set(group_list_id))
            for i in group_list_id:
                result[i] = {}
                for j in data:
                    if j["group_id"] == i:
                        if result[i].__contains__(j["sport_man"]):
                            for k in data:
                                if k["sport_man"] == j["sport_man"]:
                                    result[i][j["sport_man"]].append(k)
                        else:
                            result[i][j["sport_man"]] = []
                            for k in data:
                                if k["sport_man"] == j["sport_man"]:
                                    result[i][j["sport_man"]].append(k)
            arr = []
            for i in result:
                arr.append(i)







            return Response(arr,status=status.HTTP_200_OK)

        else:
            return Response({"message":"您没有需要审核的组"})


    @check_referee_token
    def post(self,request):
        username = request.META.get("REMOTE_USER").get("username")
        data = request.data
        if not data["D"] or not data["P"] or not data["people_id"] or not data["group"]:
            raise BadRequest
        leader = RefereeGroup.objects.filter(referee__username=username,group__id=data["group"], is_leader=True)
        if not leader:
            raise PermissionDeny
        score = Score.objects.filter(group__id=data["group"], sport_man__id=data["people_id"])
        score.update(status="已确认")
        score_dict = score.annotate(score_sum=Sum('grade'), score_max=Max('grade'), score_min=Min('grade'))
        score_avg = (score_dict["score_sum"]-score_dict["score_max"]-score_dict["score_min"])/ \
                    (score.count()-2) * score.count() + float(data["D"]) - float(data["P"])
        SportManGroup.objects.filter(sid__id=data["people_id"], gid__id=data["group"])
        if not Score.objects.filter(Q(status='待审核') | Q(status='重新打分'), group__id=data["group"] ): #     如果没有待审核，则该组为已确认
            Group.objects.filter(pk=data["group"]).update(status="已确认")

        return Response({"message":"confirm", "score":score_avg},status=status.HTTP_200_OK)

    @check_referee_token
    def delete(self, request, group_id, referee_id,people_id):
        username = request.META.get("REMOTE_USER").get("username")
        leader = RefereeGroup.objects.filter(referee__username=username, group__id=group_id, is_leader=True)
        if not leader:
            raise PermissionDeny
        group = Group.objects.filter(pk=group_id).update(status="待打分")
        score = Score.objects.filter(group__id=group_id, referee__id=referee_id,sport_man__id=people_id).update(status="重新打分")
        return Response({"message":"ok"},status=status.HTTP_200_OK)

class Rank(APIView):

    def get(self,request):
        sport_man = SportManGroup.objects.filter(gid__status="已确认").order_by("gid__id","gid__num","total_grade")
        serializer = SportManGroupSerializer(sport_man, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)













