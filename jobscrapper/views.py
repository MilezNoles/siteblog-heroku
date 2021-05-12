from django.core.paginator import Paginator
from django.shortcuts import render

from .forms import FindForm
from .models import Vacancy


def home_vacancies_view(request):

    form = FindForm()


    context = {
        "form": form,
    }
    return render(request, "jobscrapper/vacancies_home.html", context)


def vacancies_view(request):

    form = FindForm()

    city = request.GET.get("city")
    occupation = request.GET.get("occupation")
    page_obj = []
    if city or occupation:
        _filter = {}
        if city:
            _filter["city__slug"] = city
        if occupation:
            _filter["occupation__slug"] = occupation


        qs = Vacancy.objects.filter(**_filter).select_related("city").select_related("occupation")
        paginator = Paginator(qs, 10)  # Show 25 contacts per page.

        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)



    context = {
        "page_obj": page_obj,
        "form": form,
    }
    context["s"] = f"city={city}&occupation={occupation}&"
    return render(request, "jobscrapper/vacancies.html", context)

