from django.db import models, transaction
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse_lazy
from django.conf import settings

from slugify import slugify

from blog.utils import normalizer_bd
from jobscrapper.models import City, Occupation, Vacancy, Errors
from jobscrapper.parsers import hh
from jobscrapper.url_creator import url_creator_hh

User = settings.AUTH_USER_MODEL

# this is bad I know     FIX LATER
from django.contrib.auth.models import User

User._meta.get_field('email')._unique = True


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    slug = models.SlugField(max_length=255, verbose_name="Url", unique=True)
    bio = models.TextField(blank=True, verbose_name='О себе', )
    city = models.CharField(max_length=60, blank=True)
    occupation = models.CharField(max_length=200, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to="useravatars/%Y/%m/%d/", blank=True, verbose_name="profile picture", )
    send_email = models.BooleanField(default=True, verbose_name="Получать рассылку")
    url_for_hh = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"
        ordering = ["user"]

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance, slug=slugify(instance.username))

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profile.save()

    def save(self, *args, **kwargs):
        if self.city and self.occupation:
            self.url_for_hh = url_creator_hh(self.city, self.occupation)

            jobs, errors = [], []
            city = City.objects.get(name=normalizer_bd(self.city))
            occupation = Occupation.objects.get(name=normalizer_bd(self.occupation))
            jobs, e = hh(self.url_for_hh)

            if jobs != [{0: 0}]:
                all_vacancies = Vacancy.objects.filter(city=city, occupation=occupation)
                for job in jobs:

                    double_finder = all_vacancies.filter(url=job["url"])

                    if double_finder.exists():
                        continue
                    else:
                        v = Vacancy(**job, city=city, occupation=occupation)
                        v.save()
            errors += e

            if errors:
                er = Errors(data=errors)
                er.save()

        else:
            self.url_for_hh = None
        super().save(*args, **kwargs)

    def get_absolute_url(self):  # для ссылок
        return reverse_lazy("profile", kwargs={"slug": self.slug, })


class Category(models.Model):
    title = models.CharField(max_length=255, verbose_name="Category", )
    slug = models.SlugField(max_length=255, verbose_name="Url", unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):  # для ссылок
        return reverse_lazy("category", kwargs={"slug": self.slug, })

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ["title"]


class Tag(models.Model):
    title = models.CharField(max_length=50, verbose_name="Tag", )
    slug = models.SlugField(max_length=50, verbose_name="Url", unique=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):  # для ссылок
        return reverse_lazy("tag", kwargs={"slug": self.slug, })

    class Meta:
        verbose_name = "Tag"
        verbose_name_plural = "Tags"
        ordering = ["title"]


class Post(models.Model):
    title = models.CharField(max_length=255, verbose_name="Title", )
    slug = models.SlugField(max_length=255, verbose_name="Url", unique=True)
    author = models.ForeignKey(User, verbose_name="Author", on_delete=models.PROTECT, null=True, blank=True)
    content = models.TextField(verbose_name="Content", blank=True, )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Creation date", )
    photo = models.ImageField(upload_to="photos/%Y/%m/%d/", blank=True, verbose_name="Photo", )
    views = models.IntegerField(default=0, verbose_name="Views", )
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="posts", verbose_name="Category", )
    tags = models.ManyToManyField(Tag, blank=True, related_name="posts", verbose_name="Tag", )
    is_main = models.BooleanField(default=False, verbose_name="On main?")

    def __str__(self):
        return self.title

    def get_absolute_url(self):  # для ссылок
        return reverse_lazy("post", kwargs={"slug": self.slug, })

    @transaction.atomic  # для того чтобы в is_main был только один True
    def save(self, *args, **kwargs):
        if self.is_main:
            Post.objects.filter(
                is_main=True).update(is_main=False)
        super(Post, self).save(*args, **kwargs)

    class Meta:
        verbose_name = "Post"
        verbose_name_plural = "Posts"
        ordering = ["-created_at"]


class Comments(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    # if db is huge use null=True,blank=True for migrations after adding ForeignKey
    username = models.ForeignKey(User, verbose_name="Username", on_delete=models.PROTECT, blank=True)
    comment = models.TextField(verbose_name="Comment")
    created_at = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Comment"
        verbose_name_plural = "Comments"
        ordering = ['created_at']

    def __str__(self):
        return 'Comment {} by {}'.format(self.comment, self.username)
