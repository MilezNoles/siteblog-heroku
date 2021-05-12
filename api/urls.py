from django.urls import path
from api.views import *
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register("posts", PostViewSet, basename="posts")
router.register("users", UserViewSet, basename="users")
# to create auto paths for all thingies
urlpatterns = router.urls

# posts_list = PostViewSet.as_view({
#     "get": "list",
#     "post": "create",
# })
#
# post_detail = PostViewSet.as_view({
#     "get": "retrieve",
#     "put": "update",
#     "patch": "partial_update",
#     "delete": "destroy",
# })
#
# urlpatterns = [
#     path('posts/', posts_list,),
#     path('posts/<str:slug>/', post_detail ,name="posts-view"),
#
# ]
# urlpatterns = format_suffix_patterns(urlpatterns)     # for api/posts/?format= (api/json)