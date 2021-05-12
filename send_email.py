import os, sys
import django
import datetime

proj = os.path.dirname(os.path.abspath("manage.py"))
sys.path.append(proj)
os.environ["DJANGO_SETTINGS_MODULE"] = "siteblog.settings"

django.setup()

from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives

from blog.utils import normalizer_bd
from jobscrapper.models import City, Occupation, Vacancy, Errors
from siteblog.settings import EMAIL_HOST_USER

ADMIN_USER = "sgrimj@gmail.com"
empty = "<h2>К сожалению на сегодня новых вакансий нет</h2>"
today = datetime.date.today()
subject = f"Рассылка вакансий с сервиса littlebitofawesomeness.ru за {today}"
text_content = "Расылка вакансий"
from_email = EMAIL_HOST_USER

User = get_user_model()
qs = User.objects.filter(profile__send_email=True).exclude(profile__url_for_hh=None).values('profile__city',
                                                                                            'profile__occupation',
                                                                                            'email')
users_dict = {}

for i in qs:
    i["city"] = City.objects.get(name=normalizer_bd(i['profile__city']))
    i["occupation"] = Occupation.objects.get(name=normalizer_bd(i['profile__occupation']))
    users_dict.setdefault((i["city"], i["occupation"]), [])
    users_dict[(i["city"], i["occupation"])].append(i["email"])

if users_dict:

    params = {"city_id__in": [], "occupation_id__in": []}
    for pair in users_dict.keys():
        params["city_id__in"].append(pair[0])
        params["occupation_id__in"].append(pair[1])

    qs_vacancies = Vacancy.objects.filter(**params, timestamp=today).values()
    vacancies = {}
    for i in qs_vacancies:
        i["city"] = City.objects.get(pk=i['city_id'])
        i["occupation"] = Occupation.objects.get(pk=i['occupation_id'])
        vacancies.setdefault((i["city"], i["occupation"]), [])
        vacancies[(i["city"], i["occupation"])].append(i)

    for keys, emails in users_dict.items():
        rows = vacancies.get(keys, [])
        html = ""
        for row in rows:
            html += f'<h3><a href="{row["url"]}">{row["title"]}</a></h3>'
            html += f'<p> {row["description"]}</p>'
            html += f'<p> {row["company"]} | {row["salary"]}</p> <br><hr>'

        _html = html if html else empty

        for email in emails:
            to = email
            msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
            msg.attach_alternative(_html, "text/html")
            msg.send()

qs_err = Errors.objects.filter(timestamp=today)
if qs_err.exists():
    error = qs_err.first()
    data = error.data

    content = ""
    for i in data:
        content += f'<p><a href="{i["url"]}">{i["title"]}</a></p>'

    subject = f"Ошибки скраппинга {today}"
    text_content = "Ошибки скраппинга"
    to = ADMIN_USER
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(content, "text/html")
    msg.send()
