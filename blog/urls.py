from django.urls import path
from blog.views import *

urlpatterns = [
    path('', Home.as_view(), name="home"),
    path("register/", register, name="register"),
    path("login/", user_login, name="login"),
    path("logout/", user_logout, name="logout"),
    path("delete/", user_delete, name="delete"),
    path('category/<str:slug>/', PostsByCategory.as_view(), name="category"),
    path('tag/<str:slug>/', PostsByTag.as_view(), name="tag"),
    path('post/<str:slug>/',single_post, name="post"),
    path('profile/<str:slug>/',profile, name="profile"),
    path('search/',Search.as_view(), name="search"),
    # path('user/<int:pk>/',PersonalPage.as_view(), name="personal"),
]