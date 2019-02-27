from lib.rest_framework.exceptions import *
from rest_framework.views import APIView, status,Response
from lib.rest_framework.util import *
from lib.rest_framework.permissions import check_token
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
            return Response({"username":team.username,"password":team.password,"name":team.username},status=status.HTTP_201_CREATED)
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


class CompetitionView(APIView):

    @check_token
    def get(self,request):
        type = request.META.get("REMOTE_USER").get("type")
        if type != "admin":
            raise PermissionDeny
        queryset = Competition.objects.all()
        page = Pagination()
        result = page.paginate_queryset(queryset=queryset,request=request,view=self)
        serializer = TeamSerializer(result,many=True)
        return page.get_paginated_response(serializer.data)

    @check_token
    def post(self,request):
        type = request.META.get("REMOTE_USER").get("type")
        if type != "admin":
            raise PermissionDeny
        serializer = CompetitionSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
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
            serializer = CompetitionSerializer(competition)
            competition.delete()
            return Response(serializer.data,status=status.HTTP_200_OK)
        else:
            raise NotFound



