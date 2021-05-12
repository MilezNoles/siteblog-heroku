from django.db import models
from slugify import slugify

import jsonfield

class City(models.Model):
    name = models.CharField(max_length=50,
                            verbose_name="Название населенного пункта",
                            unique=True)
    slug = models.SlugField(max_length=50,blank=True, unique=True)

    class Meta:
        verbose_name = "Город"
        verbose_name_plural = "Города"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args,**kwargs)



class Occupation(models.Model):
    name = models.CharField(max_length=50,
                            verbose_name="Специальность",
                            unique=True)
    slug = models.SlugField(max_length=50, blank=True, unique=True)

    class Meta:
        verbose_name = "Специальность"
        verbose_name_plural = "Специальности"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args,**kwargs)


class Vacancy(models.Model):
    url = models.URLField(unique=True)
    title = models.CharField(max_length=250, verbose_name="Название вакансии")
    company = models.CharField(max_length=250, verbose_name="Компания")
    description = models.TextField(verbose_name="Описание вакансии")
    salary = models.CharField(max_length=100,verbose_name="Заработная плата")
    city = models.ForeignKey(City, on_delete=models.CASCADE,verbose_name="Город")
    occupation = models.ForeignKey(Occupation, on_delete=models.CASCADE, verbose_name="Язык программирования")
    timestamp = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "Вакансию"
        verbose_name_plural = "Вакансии"
        ordering = ["-timestamp"]

    def __str__(self):
        return self.title


class Errors(models.Model):
    timestamp = models.DateField(auto_now_add=True)
    data = jsonfield.JSONField()

    class Meta:
        verbose_name = "Ошибка"
        verbose_name_plural = "Ошибки"
        ordering = ["-timestamp"]

    def __str__(self):
        return str(self.timestamp)
