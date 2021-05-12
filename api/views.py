from django.contrib.auth import get_user_model
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser
from blog.models import Post
from api.serializers import PostSerializer, ThinPostSerializer, UserSerializer
from rest_framework.response import Response
from slugify import slugify
from .permissions import IsAuthorOrReadOnly
# from rest_framework.generics import GenericAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView
#can use ^ mixins + GenericAPi to get rid of funcs: get,post etc

from rest_framework.viewsets import ModelViewSet
#this ^ to merge all funcs to 1 class





class UserViewSet(ModelViewSet):
    model = get_user_model()
    queryset = model.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdminUser, )

#class + mixins based further simplification
class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = "slug"
    permission_classes = (IsAuthorOrReadOnly,)
    #use this to restrict to only get method(ALLOW: GET in api web page header)
    # http_method_names = ["get"]

    def list(self, request, *args, **kwargs):
        posts = Post.objects.all()
        context = {'request': request}
        serializer = ThinPostSerializer(posts, many=True, context=context)
        return Response(serializer.data)


    def perform_create(self, serializer):
        serializer.save(author= self.request.user, slug=slugify(self.request.POST["title"]))
