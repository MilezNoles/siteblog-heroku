from django.contrib import admin
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.utils.safestring import mark_safe

from .models import *

class PostAdminForm(forms.ModelForm):
    content = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = Post
        fields = '__all__'

class ProfileAdmin(admin.ModelAdmin):

    save_on_top = True
    list_display = ("user", "slug", "get_photo",)
    list_display_links = ("user",)
    search_fields = ("user",)
    list_filter = ("user",)

    readonly_fields = ("user","slug","get_photo","url_for_hh")
    fields =("user","slug", "bio","city","occupation", "birth_date", "profile_picture", "get_photo", "send_email","url_for_hh")

    def get_photo(self, obj):
        if obj.profile_picture:
            return mark_safe(f"<img src='{obj.profile_picture.url}' width='50'>")
        else:
            return " - "

    get_photo.short_description = "Аватар"  # Меняем вывод Getphoto в столбце админки на Preview



class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    form = PostAdminForm
    save_as = True
    save_on_top = True  # кнопки сохранить будут и вверху
    list_display = (
        "id", "title","slug", "category", "created_at", "get_photo","is_main")  # столбцы в админке
    list_display_links = ("id", "title")  # что будет ссылкой на редактирование в админке
    search_fields = ("title",)  # search in admin
    list_editable = ("category","is_main",)
    list_filter = ("category","tags")

    readonly_fields = ("views", "created_at", "get_photo","author" )  # поля которые будут только для чтения
    fields =("title","slug", "category","tags","author", "content", "photo", "get_photo","views", "created_at","is_main")


    def get_photo(self, obj):
        if obj.photo:
            return mark_safe(f"<img src='{obj.photo.url}' width='50'>")  # убирает экранирование
        else:
            return " - "

    get_photo.short_description = "Preview"  # Меняем вывод Getphoto в столбце админки на Preview


class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = (
        "id", "title", "slug",)
    list_display_links = ("id", "title")

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    list_display = (
        "id", "title", "slug",)
    list_display_links = ("id", "title")

class CommentsAdmin(admin.ModelAdmin):
    list_display = ('username', 'comment', 'post', 'created_at', 'active')
    list_filter = ('active', 'created_at')
    list_display_links = ("username",)
    search_fields = ('username', 'email', 'comment')
    list_editable = ("active",)
    fields = ('username', 'comment', 'post', 'created_at', 'active')
    readonly_fields = ("post","username", "created_at",)

    def approve_comments(self, request, queryset):
        queryset.update(active=True)



admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Comments, CommentsAdmin)
admin.site.register(Profile, ProfileAdmin)


