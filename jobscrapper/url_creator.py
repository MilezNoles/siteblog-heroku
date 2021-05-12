import codecs
import os

from siteblog.settings import BASE_DIR

rel_path = "cities.txt"
cities_path = os.path.join(BASE_DIR, rel_path)

def url_creator_hh(city:str, occupation:str):
    """
    создает ссылку для сайта hh из пары
    город + специальность
    из-за того что на хх города идут как
    area=<какой то код>
    пришлось ботом пройти от 1 до 1000,
    эти города бот закинул в cities.txt
    """
    city_code = ""
    if " " in city:
        city = city.title().replace(" ", "-")
    else: city = city.title()
    with codecs.open(cities_path, "r", "utf-8") as f:
        for line in f:
            if city in line:
                city_code = line.split(":")[1].strip("',\n")

    if not city_code:
        return "Такой город не поддерживается"

    if occupation.split(" "):
        occupation = occupation.replace(" ", "+")

    return "https://hh.ru/search/vacancy?clusters=true&area=" + city_code + "&enable_snippets=true&search_period=1&salary=&st=searchVacancy&text=" + occupation


if __name__ == "__main__":
    print(url_creator_hh("киев", "java"))

