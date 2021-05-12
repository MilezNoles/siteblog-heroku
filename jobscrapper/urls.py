from django.urls import path
from jobscrapper.views import *

urlpatterns = [
    path('', home_vacancies_view, name="vacancy-home"),
    path('list/', vacancies_view, name="vacancy"),

]