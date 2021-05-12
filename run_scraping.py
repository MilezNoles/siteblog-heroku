import os,sys
import django


proj = os.path.dirname(os.path.abspath("manage.py"))
sys.path.append(proj)
os.environ["DJANGO_SETTINGS_MODULE"] = "siteblog.settings"


django.setup()


from django.db import DatabaseError
from jobscrapper.parsers import *
from jobscrapper.models import Vacancy,City,Occupation,Errors
from blog.models import Profile
from blog.utils import normalizer_bd

#временный с суперджобом
# parsers = (
#     (hh, "https://spb.hh.ru/search/vacancy?search_period=1&clusters=true&area=2&text=Python&enable_snippets=true"),
#     (superjob, "https://spb.superjob.ru/vacancy/search/?keywords=Python&period=3&click_from=fastFilter"),
#         )


def get_unique_user_urls():
    """
    получаем сформированные ссылки на поиск вакансий для пользователей подписавшихся на рассылку
    и у которых были заполнены поля город и специальность
    """
    qs = Profile.objects.filter(send_email=True).exclude(url_for_hh=None).exclude(url_for_hh="Такой город не поддерживется")
    url_list = qs.values_list("url_for_hh", flat=True)
    return set(url_list)





jobs, errors = [],[]

for url in get_unique_user_urls():
    qs = Profile.objects.filter(url_for_hh=url).first()
    city = City.objects.get(name=normalizer_bd(qs.city))
    occupation = Occupation.objects.get(name=normalizer_bd(qs.occupation))
    jobs,e = hh(url)
    if jobs == [{0: 0}]:
        continue
    for job in jobs:
        v = Vacancy(**job, city=city, occupation=occupation)
        try:
            v.save()
        except DatabaseError:
            pass

    errors+=e

if errors:
    er = Errors(data=errors)
    er.save()

# with codecs.open("jobs.txt","w+", "utf-8") as f:
#     f.write(str(jobs))
# with codecs.open("errors.txt","w+", "utf-8") as f:
#     f.write(str(errors))
