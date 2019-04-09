from django.db import models

# Create your models here.

class Team(models.Model):
    username = models.CharField(verbose_name="账号",max_length=32,unique=True,default="")
    password = models.CharField(verbose_name="密码", max_length=32,default='')
    name = models.CharField(verbose_name="代表队队名",max_length=32,default='', unique=True)
    file = models.FileField(upload_to='file/',default="file/default")

    class Meta:
        verbose_name = '代表队表'
        verbose_name_plural = '代表队表'
        ordering = ['id',]

    def __str__(self):
        return '%s %s' % (self.username, self.name)


class Competition(models.Model):
    NAME_CHOICE=(
        ("单杠", "单杠"),
        ("双杠", "双杠"),
        ("吊环", "吊环"),
        ("自由体操", "自由体操"),
        ("鞍马", "鞍马"),
        ("蹦床", "蹦床"),


        ("跳马","跳马"),
        ("高低杠", "高低杠"),
        ("平衡木", "平衡木"),

    )
    SEX = (
        ("男", "男"),
        ("女", "女"),
    )
    AGEGROUP = (
        ("7-8","7-8"),
        ("9-10","9-10"),
        ("11-12", "11-12"),

     )
    name = models.CharField(max_length=32, choices=NAME_CHOICE)
    sex = models.CharField(verbose_name="性别",default="男", max_length=32, choices=SEX)
    age_group = models.CharField(verbose_name="年龄",default="7-8", max_length=32, choices=AGEGROUP)

    class Meta:
        verbose_name = '比赛项目表'
        verbose_name_plural = '比赛项目表'
        # index_together = ["course_name", "teacher"]  # 组合索引
        unique_together = ["name", "sex", "age_group"]  #联合唯一
        ordering = ['id',]      #防止rest_framework.PageNumberPagination 报错

    def __str__(self):
        return '%s子组 %s %s' % (self.sex, self.age_group,self.name)

class SportMan(models.Model):
    AGEGROUP = (
        ("7-8", "7-8"),
        ("9-10", "9-10"),
        ("11-12", "11-12"),
    )
    SEX = (
        ("男", "男"),
        ("女", "女"),
    )

    name = models.CharField(verbose_name="姓名",max_length=32,db_index=True)
    id_number = models.CharField(verbose_name="身份证号码", max_length=18, default="", unique=True)
    age = models.IntegerField(verbose_name="年龄", blank=True, null=True)
    sex = models.CharField(verbose_name="性别", max_length=32, default="男", choices=SEX)
    age_group = models.CharField(verbose_name="组别",default="7-8岁",choices=AGEGROUP,max_length=32)
    grade = models.FloatField(verbose_name="文化分数", blank=True, null=True)
    team = models.ForeignKey("Team", verbose_name="所属代表队",blank=True,null=True,on_delete=models.SET_NULL,related_name='sport_man_team')
    number = models.IntegerField(verbose_name="运动员号码", unique=True, blank=True, null=True)
    competition_group = models.ManyToManyField("Group", verbose_name="报名分组", through='SportManGroup', through_fields=("sid", "gid"), related_name='sport_man')

    # phone = models.CharField(verbose_name="手机号码", max_length=32,blank=True, null=True)
    # team = models.ForeignKey("Team",blank=True, null=True,on_delete=models.SET_NULL)
    # sex = models.CharField(verbose_name="性别", max_length=32,default="男", choices=SEX)
    # age = models.IntegerField(verbose_name="年龄",blank=True, null=True)
    # group = models.ForeignKey("Group",blank=True,null=True,on_delete=models.SET_NULL)

    class Meta:
        verbose_name = '运动员表'
        verbose_name_plural = '运动员表'
        ordering = ['id',]      #防止rest_framework.PageNumberPagination 报错

    def __str__(self):
        return '%s %s ' % (self.name, self.team.name)


class Referee(models.Model):
    username = models.CharField(verbose_name="账号", max_length=32,unique=True)
    password = models.CharField(verbose_name="密码", max_length=32, default='')
    name = models.CharField(verbose_name="姓名", max_length=32, db_index=True)
    id_number = models.CharField(verbose_name="身份证号码", max_length=18, default="", unique=True)
    phone = models.CharField(verbose_name="手机号码", max_length=32, default="")
    team = models.ForeignKey("Team", verbose_name="所属代表队", blank=True, null=True, on_delete=models.SET_NULL,related_name='referee_team')
    group = models.ManyToManyField("Group",verbose_name="赛事分组", through='RefereeGroup', through_fields=("referee", "group"), related_name='referee_group')


    class Meta:
        verbose_name = '裁判表'
        verbose_name_plural = '裁判表'
        ordering = ['id',]

    def __str__(self):
        return '%s %s ' % (self.username, self.name)

class Coach(models.Model):
    SEX = (
        ("男", "男"),
        ("女", "女"),
    )
    name = models.CharField(verbose_name="姓名", max_length=32, db_index=True)
    id_number = models.CharField(verbose_name="身份证号码", max_length=18, default="", unique=True)
    phone = models.CharField(verbose_name="手机号码", max_length=32, default="")
    team = models.ForeignKey("Team", verbose_name="所属代表队", blank=True, null=True, on_delete=models.SET_NULL,related_name="coach_team")


    class Meta:
        verbose_name = '教练表'
        verbose_name_plural = '教练表'
        ordering = ['id',]

    def __str__(self):
        return '%s %s ' % (self.name, self.team.name)

class LeaderAndDoctor(models.Model):
    PLACE=(
        ("领队", "领队"),
        ("队医", "队医"),
    )
    name = models.CharField(verbose_name="姓名", max_length=32, db_index=True)
    id_number = models.CharField(verbose_name="身份证号码", max_length=18, default="", unique=True)
    phone = models.CharField(verbose_name="手机号码", max_length=32, default="")
    place = models.CharField(verbose_name="职位",max_length=32,choices=PLACE,default="领队")
    team = models.ForeignKey("Team", verbose_name="所属代表队", blank=True, null=True, on_delete=models.SET_NULL,related_name='leader_team')

    class Meta:
        verbose_name = '领队-队医表'
        verbose_name_plural = '领队-队医表'
        ordering = ['id',]

    def __str__(self):
        return '%s %s ' % (self.name, self.team.name)


class SportManGroup(models.Model):
    sid = models.ForeignKey("SportMan",blank=True, null=True, on_delete=models.SET_NULL)
    gid = models.ForeignKey("Group",blank=True, null=True, on_delete=models.SET_NULL)
    # competition = models.ForeignKey("Competition", verbose_name="比赛项目", on_delete=models.CASCADE)
    total_grade = models.FloatField(verbose_name="最终得分", blank=True, null=True)
    d = models.FloatField(verbose_name="奖励分", blank=True, null=True)
    p = models.FloatField(verbose_name="惩罚分", blank=True, null=True)

    class Meta:
        verbose_name = '运动员比赛成绩'
        verbose_name_plural = '运动员比赛成绩'


class Group(models.Model):
    LEVEL=(
        ("初赛","初赛"),
        ("决赛", "决赛"),
    )
    STATUS = (
        ("未开始","未开始"),
        ("待打分","待打分"),
        ("重新打分", "重新打分"),
        ("待审核", "待审核"),
        ("已确认", "已确认"),
    )
    num = models.IntegerField(verbose_name="项目组号", default=0)
    competition = models.ForeignKey("Competition", verbose_name="项目",blank=True,null=True, on_delete=models.SET_NULL, related_name='group_competition')
    level = models.CharField(verbose_name="初赛/决赛",default="初赛",max_length=32,choices=LEVEL)
    status = models.CharField(verbose_name="状态",max_length=32,default="未开始",choices=STATUS)

    class Meta:
        verbose_name = '赛事分组表'
        verbose_name_plural = '赛事分组表'
        unique_together = ["num", "competition","level"]

    def __str__(self):
        return '%s %s组' % (self.competition.name,self.num)

class RefereeGroup(models.Model):
    referee = models.ForeignKey(Referee,verbose_name="裁判",blank=True,null=True, on_delete=models.SET_NULL)
    group = models.ForeignKey("Group",verbose_name="赛事分组",blank=True, null=True, on_delete=models.SET_NULL)
    is_leader = models.BooleanField(verbose_name="小组总裁判",default=False)

    class Meta:
        verbose_name = '裁判分组表'
        verbose_name_plural = '裁判分组表'


class Score(models.Model):
    STATUS = (
        ("重新打分", "重新打分"),
        ("待审核", "待审核"),
        ("已确认", "已确认"),
    )
    referee = models.ForeignKey(Referee, verbose_name="裁判", blank=True, null=True, on_delete=models.SET_NULL)
    group = models.ForeignKey(Group, verbose_name="赛事分组", blank=True, null=True, on_delete=models.SET_NULL)
    sport_man = models.ForeignKey(SportMan, verbose_name="运动员",blank=True, null=True, on_delete=models.SET_NULL)
    grade = models.FloatField()
    status = models.CharField(verbose_name="状态", max_length=32, default="待审核", choices=STATUS)

    class Meta:
        verbose_name = '打分表'
        verbose_name_plural = '打分表'
        unique_together = ["referee", "group", "sport_man"]



