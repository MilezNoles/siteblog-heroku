from django import forms

from jobscrapper.models import City, Occupation


class FindForm(forms.Form):
    city = forms.ModelChoiceField(queryset=City.objects.all(),
                                  widget=forms.Select(attrs={'class': "form-control",}),
                                  to_field_name="slug",
                                  required=False, label="Город")

    occupation = forms.ModelChoiceField(queryset=Occupation.objects.all(),
                                      widget=forms.Select(attrs={'class': "form-control",}),
                                      to_field_name="slug",
                                      required=False, label="Специальность")
