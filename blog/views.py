from django.contrib.auth import login, logout, get_user_model
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.core.mail import send_mail
from django.db.models import F

from blog.forms import *
from blog.models import *

from jobscrapper.models import *
from .utils import *
User = get_user_model()


def register(request):
    if request.method == "POST":
        form = UserRegister(request.POST)  # связь формы с данными
        if form.is_valid():
            user = form.save()
            login(request, user)
            slug = user.profile.slug

            mail = send_mail(get_mail_subject(form.cleaned_data["username"]),
                             get_mail_context(form.cleaned_data["username"], form.cleaned_data["email"],
                                              form.cleaned_data["password1"]),
                             "testsubj88@yandex.ru", ["sgrimj@gmail.com", form.cleaned_data["email"]],
                             fail_silently=True)
            # if mail:
            #      return redirect("profile")
            # else:
            #     print("something got wrong")
            return redirect("profile", slug)
    # /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
    else:
        form = UserRegister()

    context = {
        "form": form,
    }
    return render(request, "blog/register.html", context)


def user_login(request):
    if request.method == "POST":
        form = UserLogin(data=request.POST)  # для логина обязательна data=
        if form.is_valid():
            user = form.get_user()
            login(request, user)

            return redirect("home")


    else:
        form = UserLogin()

    context = {
        "form": form,
    }
    return render(request, "blog/login.html", context)


def user_logout(request):
    logout(request)
    return redirect("login")


def user_delete(request):
    user = request.user
    if request.method == "POST":
        qs = User.objects.get(pk=user.pk)
        qs.delete()
    return redirect("home")


@transaction.atomic
def profile(request, slug):
    template_name = 'blog/profile.html'
    profile = get_object_or_404(Profile, slug=slug)

    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        # request.FILES for files in form

        if profile_form.is_valid():
            temp_form = profile_form.save(commit=False)

            # if profile city not in db then add
            if temp_form.city:
                # проверяем есть ли данный город в бд городов по hh
                check_url = url_creator_hh(temp_form.city, "TEMP")

                if check_url == "Такой город не поддерживается":
                    temp_form.city = temp_form.city + ": временно не поддерживается"
                else:
                    check_city = normalizer_bd(profile_form.instance.city)
                    city = City.objects.filter(name=check_city)
                    if not city:
                        temp = City(name=check_city)
                        temp.save()

            # if profile occupation not in db then add
            if temp_form.occupation:
                check_occupation = normalizer_bd(profile_form.instance.occupation)
                occupation = Occupation.objects.filter(name=check_occupation)
                if not occupation:
                    temp = Occupation(name=check_occupation)
                    temp.save()


            temp_form.save()

            return redirect("profile", slug=slug)
    else:
        profile_form = ProfileForm(instance=profile)

    context = {'profile': profile,
               'form': profile_form,
               }

    return render(request, template_name, context)


class Home(ListView):
    model = Post
    template_name = "blog/index.html"
    context_object_name = "posts"
    paginate_by = 4

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        context["title"] = "Blog Design"
        context["main"] = Post.objects.get(is_main=True)

        return context


class PostsByCategory(ListView):
    template_name = "blog/category.html"
    context_object_name = "posts"
    paginate_by = 4
    allow_empty = False

    def get_queryset(self):
        return Post.objects.filter(category__slug=self.kwargs["slug"])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = Category.objects.get(slug=self.kwargs["slug"])
        return context


class PostsByTag(ListView):
    template_name = "blog/category.html"
    context_object_name = "posts"
    paginate_by = 4
    allow_empty = False

    def get_queryset(self):
        return Post.objects.filter(tags__slug=self.kwargs["slug"])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "All posts by tag: " + str(Tag.objects.get(slug=self.kwargs["slug"]))
        return context


def single_post(request, slug):
    template_name = 'blog/single.html'
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(active=True).select_related("username")  # reduce SQL queries
    new_comment = None
    post.views = F("views") + 1
    post.save()
    post.refresh_from_db()
    # Comments
    if request.method == 'POST':
        comment_form = CommentsForm(data=request.POST)
        if comment_form.is_valid():
            # Setting user to current logged in user
            comment_form.instance.username = request.user
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            if request.user.is_staff:
                new_comment.active = True
                new_comment.save()
            else:
                new_comment.save()
    else:
        comment_form = CommentsForm()

    context = {'post': post,
               'comments': comments,
               'new_comment': new_comment,
               'form': comment_form}
    return render(request, template_name, context)


class Search(ListView):
    template_name = "blog/search.html"
    context_object_name = "posts"
    paginate_by = 4

    def get_queryset(self):
        return Post.objects.filter(title__icontains=self.request.GET.get("s"))

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context["s"] = f"s={self.request.GET.get('s')}&"
        return context
