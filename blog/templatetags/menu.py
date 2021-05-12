from django import template
from blog.models import Category
from django.db.models import *


register = template.Library()



@register.inclusion_tag("blog/menu_tpl.html")
def show_menu(menu_class='menu', ul_class=""):
    categories = Category.objects.all()            # обращаемся в кэш, если там нет ничего то заполняем на 500сек
    return {"categories": categories, "menu_class": menu_class, "ul_class": ul_class }