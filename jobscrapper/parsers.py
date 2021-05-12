import requests
import codecs
from bs4 import BeautifulSoup as BS
from random import randint


headers = [
    {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36"},
    {"User-Agent": "Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10.12; rv:82.0) Gecko/20100101 Firefox/82.0"},
    {"User-Agent": "Mozilla/5.0 (X11; Linux i686; rv:86.0) Gecko/20100101 Firefox/86.0"},
    {
        "User-Agent": "Mozilla/5.0 (X11; U; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.87 Safari/537.36"},
]

jobs = []
errors = []


def hh(url):
    jobs = []
    errors = []

    resp = requests.get(url, headers=headers[randint(0, 3)])
    if resp.status_code == 200:

        soup = BS(resp.content, "html.parser")

        no_new = soup.find("p", attrs={"class": "vacancysearch-xs-header-text"})

        #sometimes hh.ru bugges out and gives particially empty page which causes AttributeError, so if that bug occurs:
        if no_new == None:
            jobs.append({0: 0})
            errors.append({
                "url": url,
                "title": "Page is empty(None error)",
            })
            return jobs, errors


        if "ничего не найдено" in no_new.text:
            jobs.append({0: 0})
            errors.append({
                "url": url,
                "title": "Page is empty",
            })
            return jobs, errors


        main_div = soup.find("div", attrs={"class": "vacancy-serp"})
        div_list = main_div.find_all("div", attrs={"class": "vacancy-serp-item"})
        for div in div_list:
            title = div.find("a", attrs={"class": "bloko-link"})

            url_to_job = title["href"]

            title = title.text

            company = div.find("div", attrs={"class": "vacancy-serp-item__meta-info-company"}).text

            description = div.find("div", attrs={"class": "g-user-content"}).text

            salary_check = div.find("span", attrs={"data-qa": "vacancy-serp__vacancy-compensation"})
            if salary_check:
                salary = salary_check.text
            else:
                salary = "зп не указана"

            jobs.append({
                "title": title,
                "url": url_to_job,
                "company": company,
                "description": description,
                "salary": salary,
            })

    else:
        errors.append({
            "url": url,
            "title": "Page do not responsed",
            "code": "resp.status_code",
        })
    return jobs, errors


def superjob(url):
    jobs = []
    errors = []
    base_url = "https://spb.superjob.ru"

    resp = requests.get(url, headers=headers[randint(0, 3)])
    if resp.status_code == 200:
        soup = BS(resp.text, "html.parser")

        no_new_jobs = soup.find("div", attrs={"class": "_1h3Zg _2dazi _2hCDz _2ZsgW _21a7u"})

        if not no_new_jobs:

            main_div = soup.find("div", attrs={"class": "_1ID8B"})
            div_list = main_div.find_all("div", attrs={"class": "f-test-search-result-item"})

            for div in div_list:

                title = div.find("div", attrs={"class": "_1h3Zg _2rfUm _2hCDz _21a7u"})
                if not title:
                    continue

                url_to_job = base_url + title.a["href"]

                title = title.text

                company = div.find("span", attrs={"class": "f-test-text-vacancy-item-company-name"}).text

                description = div.find("span", attrs={"class": "_1h3Zg _38T7m e5P5i _2hCDz _2ZsgW _2SvHc"}).text

                salary_check = div.find("span", attrs={"class": "f-test-text-company-item-salary"})
                if salary_check:
                    salary = salary_check.text
                else:
                    salary = "зп не указана"

                jobs.append({
                    "title": title,
                    "url": url_to_job,
                    "company": company,
                    "description": description,
                    "salary": salary,
                })

        else:
            jobs.append({0: 0})
            errors.append({
                "url": url,
                "title": "Page is empty",
            })
            return jobs, errors

    else:
        errors.append({
            "url": url,
            "title": "Page do not responsed",
            "code": "resp.status_code",
        })
    return jobs, errors


if __name__ == "__main__":
    url = "https://spb.superjob.ru/vacancy/search/?keywords=Python&period=3&click_from=fastFilter"
    url2 = "https://hh.ru/search/vacancy?clusters=true&area=115&enable_snippets=true&search_period=1&salary=&st=searchVacancy&text=java"
    url3 = "https://spb.hh.ru/search/vacancy?search_period=1&clusters=true&area=2&text=Python&enable_snippets=true"
    url4 = "https://hh.ru/search/vacancy?clusters=true&area=219&enable_snippets=true&search_period=1&salary=&st=searchVacancy&text=java+senior"
    jobs, errors = hh(url2)
    with codecs.open("jobs.txt", "w+", "utf-8") as f:
        f.write(str(jobs))
    with codecs.open("errors.txt", "w+", "utf-8") as f:
        f.write(str(errors))
