
from rest_framework.serializers import IntegerField,EmailField,Serializer,ModelSerializer,\
    ImageField, HyperlinkedIdentityField,SlugRelatedField, SerializerMethodField, ValidationError
from django.contrib.auth import get_user_model
from blog.models import Post
from django.contrib.auth.hashers import make_password



class UserSerializer(ModelSerializer):
    email = EmailField(max_length=255, required=True,)



    class Meta:
        model = get_user_model()
        queryset = model.objects.all()
        fields = ("id", "username","email", "password", "is_superuser")
        extra_kwargs = {"password": {"write_only": True}}  #for user password


    def create(self, validated_data):
        user = self.Meta.model(**validated_data)
        user.password = make_password(user.password)
        #temporary email handler
        users = self.Meta.queryset
        lower_email = user.email.lower()
        if users.filter(email__iexact=lower_email).exists():
            raise ValidationError("This email already exists")

        user.save()
        return user
        
    def update(self, instance, validated_data):
        instance.set_password(validated_data.pop("password", ""))
        #temporary email handler
        user = self.Meta.model(**validated_data)
        users = self.Meta.queryset
        lower_email = user.email.lower()
        if users.filter(email__iexact=lower_email).exists():
            raise ValidationError("This email already exists")
        return super().update(instance, validated_data)

    # def validate_email(self, value):
    #     lower_email = value.lower()
    #     users = self.Meta.queryset
    #     if users.filter(email__iexact=lower_email).exists():
    #         raise ValidationError("This email already exists")
    #     return lower_email
        
        

class PostSerializer(ModelSerializer):
    author = SerializerMethodField(read_only=True)       # set read only
    views = SerializerMethodField(read_only=True)
    slug = SerializerMethodField(read_only=True)

    def get_author(self,obj):
        return obj.author.username

    def get_views(self,obj):
        return obj.views

    def get_slug(self,obj):
        return obj.slug

    class Meta:
        model = Post
        fields = "__all__"


class ThinPostSerializer(ModelSerializer):   #for shorter view
    url = HyperlinkedIdentityField(view_name="posts-detail", lookup_field="slug")     #for urls in api view page
    class Meta:
        model = Post
        fields = ("id", "title", "url")






# class PostSerializer(Serializer):
#     id = IntegerField(read_only=True)
#     title = CharField(max_length=255,)
#     # slug = SlugField(max_length=255, unique=True)
#     author = CharField(max_length=100,)
#     content = CharField(required=False, allow_blank=True)
#     photo = ImageField()
#
#     def create(self, validated_data):
#        return Post.objects.create(**validated_data)              #inpacked data
#
#     def update(self, instance, validated_data):
#         instance.title = validated_data.get("title",instance.title)
#         instance.author = validated_data.get("author",instance.author )
#         instance.content = validated_data.get("content",instance.content)
#         instance.photo = validated_data.get("photo", instance.photo)
#         instance.save()
#         return instance

