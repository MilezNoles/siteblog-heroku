from django import template
from blog.models import Post, Tag
from django.db.models import *


register = template.Library()

@register.inclusion_tag("blog/popular_posts_tpl.html")
def get_popular(cnt=3):
    posts = Post.objects.order_by("-views")[:cnt].select_related("author")
    return {"posts": posts}

@register.inclusion_tag("blog/tags_tpl.html")
def get_tags():
    tags = Tag.objects.annotate(cnt=Count("posts")).order_by('-cnt')
    return {"tags": tags}
