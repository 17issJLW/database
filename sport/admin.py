from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(Team)
admin.site.register(LeaderAndDoctor)
admin.site.register(Referee)

class SportManGroupInline(admin.TabularInline):
    model = SportManGroup
    extra = 1

class SportManAdmin(admin.ModelAdmin):
    list_display = ("name","age","sex")
    inlines = (SportManGroup,)

class GroupAdmin(admin.ModelAdmin):
    inlines = (SportManGroup,)

#
#
# class CoachGroupInline(admin.TabularInline):
#     model = CoachGroup
#     extra = 1
#
# class CoachAdmin(admin.ModelAdmin):
#     inlines = (CoachGroup,)
#
# class GroupAdmin(admin.ModelAdmin):
#     inlines = (CoachGroup,)

admin.site.register(Competition)
admin.site.register(SportMan)

admin.site.register(Group)
admin.site.register(Coach)
#
admin.site.register(SportManGroup)
admin.site.register(CoachGroup)