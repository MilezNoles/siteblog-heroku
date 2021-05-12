from django.contrib import admin

# Register your models here.
from .models import *


class CityAdmin(admin.ModelAdmin):
    list_display = ('name','slug')

class OccupationAdmin(admin.ModelAdmin):
    list_display = ('name','slug')

# class VacancyAdmin(admin.ModelAdmin):
#         list_display = ()




admin.site.register(City, CityAdmin)
admin.site.register(Occupation, OccupationAdmin)
admin.site.register(Vacancy)
admin.site.register(Errors)
